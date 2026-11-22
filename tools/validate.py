"""PIXM validation: the authoritative check (CLAUDE.md §10).

Checks
  1. The PIXM schema set compiles (all schema/0.5/PIXM_*.xsd together).
  2. Every example is well-formed and valid against the schema.
  3. Lint of the PIXM schema files (see tools/README.md for the rules).

Lint warnings (3) are compared with tools/lint-baseline.json, the recorded
list of known legacy issues. The run FAILS on any error, or on any warning
that is not in the baseline.

Usage
  python tools/validate.py                      # everything
  python tools/validate.py examples/X/file.xml  # schema + lint + only these examples
  python tools/validate.py --lint-only          # lint only, no compilation
  python tools/validate.py --show-known         # also list baseline (known) findings
  python tools/validate.py --prune-baseline     # remove fixed entries from the baseline
  python tools/validate.py --init-baseline      # create the baseline (CCB-approved only)
"""

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter

from lxml import etree

import schema_cache

REPO_ROOT = schema_cache.REPO_ROOT
SCHEMA_DIR = schema_cache.SCHEMA_DIR
SCHEMA_GLOB = os.path.join(SCHEMA_DIR, 'PIXM_*.xsd')
EXAMPLES_DIR = os.path.join(REPO_ROOT, 'examples')
BASELINE = os.path.join(REPO_ROOT, 'tools', 'lint-baseline.json')

XS = 'http://www.w3.org/2001/XMLSchema'
PIXM_NS = 'http://www.pixm.aero/schema/0.5'
Q = '{%s}' % XS

UPPER_CAMEL_TYPE = re.compile(r'^[A-Z][A-Za-z0-9]*Type$')
LOWER_CAMEL = re.compile(r'^[a-z][A-Za-z0-9]*$')
UPPER_SNAKE = re.compile(r'^[A-Z0-9][A-Z0-9_]*$')


def rel(path):
    return os.path.relpath(path, REPO_ROOT).replace(os.sep, '/')


class Finding:
    """One error or warning. `key` is stable (no line numbers) for the baseline."""

    def __init__(self, severity, rule, where, message, line=None):
        self.severity = severity  # 'error' | 'warning'
        self.rule = rule
        self.where = where
        self.message = message
        self.line = line

    @property
    def key(self):
        return '%s|%s|%s' % (self.rule, self.where, self.message)

    def __str__(self):
        loc = self.where + (':%d' % self.line if self.line else '')
        return '%-7s %-14s %s  %s' % (self.severity.upper(), self.rule, loc, self.message)


# ---------------------------------------------------------------------------
# Lint
# ---------------------------------------------------------------------------

def has_doc(el):
    for doc in el.findall('%sannotation/%sdocumentation' % (Q, Q)):
        if (doc.text or '').strip() or len(doc):
            return True
    return False


def qname_ns(el, value):
    """Namespace and local name of a QName attribute value, using el's nsmap."""
    prefix, _, local = value.rpartition(':')
    return el.nsmap.get(prefix or None), prefix, local


def enclosing_name(el):
    """Name of the nearest named ancestor component (for messages)."""
    p = el.getparent()
    while p is not None:
        if p.get('name') and p.tag in (Q + 'complexType', Q + 'simpleType', Q + 'element'):
            return p.get('name')
        p = p.getparent()
    return '?'


def lint_file(path, findings, index):
    tree = etree.parse(path)
    root = tree.getroot()
    fname = rel(path)

    def warn(rule, message, el):
        findings.append(Finding('warning', rule, fname, message, el.sourceline))

    for el in root.iter(etree.Element):
        tag = el.tag
        name = el.get('name')
        parent = el.getparent()
        is_global = parent is root

        # Named global types
        if tag in (Q + 'complexType', Q + 'simpleType') and is_global and name:
            index['types'][name] = el
            index['files'][name] = fname
            if not UPPER_CAMEL_TYPE.match(name):
                warn('NAME-TYPE', '%s: type names are UpperCamelCase ending in Type' % name, el)
            if not has_doc(el):
                warn('DOC', '%s: missing xs:documentation' % name, el)

        # Global elements
        if tag == Q + 'element' and is_global and name:
            index['elements'][name] = el
            index['files']['element:' + name] = fname

        # Local element declarations (properties)
        if tag == Q + 'element' and not is_global:
            owner = enclosing_name(el)
            label = '%s/%s' % (owner, name or el.get('ref'))
            if name:
                if not LOWER_CAMEL.match(name):
                    warn('NAME-PROP', '%s: property names are lowerCamelCase' % label, el)
                if not has_doc(el):
                    warn('DOC', '%s: missing xs:documentation' % label, el)
            if el.get('minOccurs') is None or el.get('maxOccurs') is None:
                warn('OCCURS', '%s: minOccurs/maxOccurs not both explicit' % label, el)
            if el.find(Q + 'complexType') is not None or el.find(Q + 'simpleType') is not None:
                warn('ANON', '%s: anonymous inline type' % label, el)
            t = el.get('type')
            if t:
                ns, _, local = qname_ns(el, t)
                if ns == XS:
                    warn('PRIMITIVE', '%s: XSD primitive %s used directly' % (label, local), el)

        # Enumeration literals
        if tag == Q + 'enumeration':
            owner = enclosing_name(el)
            value = el.get('value', '')
            if not UPPER_SNAKE.match(value):
                warn('NAME-LITERAL', '%s/%s: literals are UPPER_SNAKE_CASE' % (owner, value), el)
            if not has_doc(el):
                warn('DOC', '%s/%s: missing xs:documentation' % (owner, value), el)

        # pixm: prefix on references to PIXM components
        for attr in ('type', 'base', 'ref', 'substitutionGroup', 'itemType'):
            v = el.get(attr)
            if v:
                ns, prefix, local = qname_ns(el, v)
                if ns == PIXM_NS and prefix != 'pixm':
                    warn('PREFIX', '%s="%s": use the pixm: prefix' % (attr, v), el)

        # Measures: units rule
        if tag == Q + 'complexType' and is_global and name and name.startswith('Val') \
                and name.endswith('Type') and not name.endswith('BaseType'):
            uom = el.find('.//%sattribute[@name="uom"]' % Q)
            if uom is not None and uom.get('use') != 'required':
                warn('UNITS', '%s: uom must be use="required"' % name, el)
            if uom is None:
                index['dimensionless'].append((name, el, fname))


def lint_cross(findings, index):
    types, elements, files = index['types'], index['elements'], index['files']

    def warn(rule, message, el):
        name = el.get('name')
        key = name if el.tag != Q + 'element' else 'element:' + name
        findings.append(Finding('warning', rule, files.get(key, '?'), message, el.sourceline))

    for name, el in sorted(types.items()):
        for fam in ('Code', 'Val', 'Text'):
            if name.startswith(fam) and name.endswith('BaseType'):
                partner = name[:-len('BaseType')] + 'Type'
                if partner not in types:
                    warn('PAIR', '%s has no matching %s' % (name, partner), el)
            elif name.startswith(fam) and name.endswith('Type') and not name.endswith('BaseType') \
                    and el.tag == Q + 'complexType':
                partner = name[:-len('Type')] + 'BaseType'
                if partner not in types:
                    warn('PAIR', '%s has no matching %s' % (name, partner), el)
        if name.endswith('TimeSliceType') and name != 'AbstractPIXMTimeSliceType':
            base = name[:-len('TimeSliceType')]
            if base + 'Type' not in types:
                warn('PAIR', '%s has no matching feature type %sType' % (name, base), el)
            for elname in (base, base + 'TimeSlice'):
                ge = elements.get(elname)
                if ge is None:
                    warn('PAIR', '%s: no global element %s' % (name, elname), el)
                elif not ge.get('substitutionGroup'):
                    warn('PAIR', 'element %s has no substitutionGroup' % elname, ge)

    for name, el, fname in index['dimensionless']:
        base = types.get(name[:-len('Type')] + 'BaseType')
        docs = ' '.join(''.join(d.itertext()) for target in (el, base) if target is not None
                        for d in target.findall('%sannotation/%sdocumentation' % (Q, Q)))
        if 'dimensionless' not in docs.lower():
            warn('UNITS', '%s: no uom and not documented as dimensionless' % name, el)


def run_lint():
    findings = []
    index = {'types': {}, 'elements': {}, 'files': {}, 'dimensionless': []}
    for path in sorted(glob.glob(os.path.join(SCHEMA_DIR, '*.xsd'))):
        try:
            lint_file(path, findings, index)
        except etree.XMLSyntaxError as exc:
            findings.append(Finding('error', 'WELLFORMED', rel(path), str(exc)))
    lint_cross(findings, index)
    return findings


# ---------------------------------------------------------------------------
# Schema compilation and example validation
# ---------------------------------------------------------------------------

def compile_schema(findings):
    import xmlschema
    if not schema_cache.cache_present():
        print('External schema cache missing; fetching (python tools/fetch_schemas.py)...')
        _, _, failures = schema_cache.fetch(log=lambda m: None)
        for url, msg in failures:
            findings.append(Finding('error', 'FETCH', url, msg))
    # Compile every PIXM schema file as one set, so examples may use elements
    # from any of them (e.g. PIXM_Messages.xsd, which includes PIXM_Features.xsd).
    sources = sorted(glob.glob(SCHEMA_GLOB))
    try:
        return xmlschema.XMLSchema(sources, uri_mapper=schema_cache.uri_mapper)
    except Exception as exc:
        findings.append(Finding('error', 'SCHEMA', rel(SCHEMA_DIR),
                                str(exc).strip().splitlines()[0]))
        return None


def validate_examples(schema, paths, findings):
    for path in paths:
        where = rel(path)
        try:
            etree.parse(path)
        except etree.XMLSyntaxError as exc:
            findings.append(Finding('error', 'WELLFORMED', where, 'not well-formed: %s' % exc))
            continue
        if schema is None:
            continue
        try:
            errors = list(schema.iter_errors(path))
        except Exception as exc:
            findings.append(Finding('error', 'EXAMPLE', where, str(exc).strip().splitlines()[0]))
            continue
        for err in errors:
            reason = (err.reason or str(err)).strip().splitlines()[0]
            path_in_doc = getattr(err, 'path', None) or ''
            findings.append(Finding('error', 'EXAMPLE', where,
                                    '%s: %s' % (re.sub(r'\[\d+\]', '', path_in_doc), reason),
                                    getattr(getattr(err, 'elem', None), 'sourceline', None)))


# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------

def load_baseline():
    if not os.path.isfile(BASELINE):
        return None
    with open(BASELINE, encoding='utf-8') as f:
        return Counter(json.load(f)['known'])


def write_baseline(counter):
    known = sorted(counter.elements())
    with open(BASELINE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'_comment': 'Known legacy issues. Remove entries when fixed '
                               '(--prune-baseline). Adding entries needs CCB approval.',
                   'known': known}, f, indent=1, ensure_ascii=False)
        f.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('examples', nargs='*', help='validate only these example files')
    parser.add_argument('--lint-only', action='store_true')
    parser.add_argument('--show-known', action='store_true',
                        help='also list findings that are in the baseline')
    parser.add_argument('--prune-baseline', action='store_true',
                        help='remove baseline entries that no longer occur')
    parser.add_argument('--init-baseline', action='store_true',
                        help='create the baseline from current findings (only if none exists)')
    args = parser.parse_args()

    findings = run_lint()
    partial = bool(args.examples) or args.lint_only
    if not args.lint_only:
        schema = compile_schema(findings)
        if args.examples:
            paths = [os.path.abspath(p) for p in args.examples]
        else:
            paths = sorted(glob.glob(os.path.join(EXAMPLES_DIR, '**', '*.xml'), recursive=True))
        validate_examples(schema, paths, findings)

    # Only warnings can be baselined; errors are always new (CCB decision).
    current = Counter(f.key for f in findings if f.severity == 'warning')

    if args.init_baseline:
        if os.path.isfile(BASELINE):
            print('Baseline already exists; refusing to overwrite. Use --prune-baseline.')
            return 2
        if partial:
            print('--init-baseline needs a full run (no file arguments, no --lint-only).')
            return 2
        write_baseline(current)
        print('Baseline created with %d entries: %s' % (sum(current.values()), rel(BASELINE)))
        return 0

    baseline = load_baseline() or Counter()
    remaining = baseline.copy()
    new = []
    for f in findings:
        if f.severity == 'warning' and remaining[f.key] > 0:
            remaining[f.key] -= 1
            f.known = True
        else:
            f.known = False
            new.append(f)
    fixed = +remaining  # baseline entries not seen in this run

    if args.prune_baseline:
        if partial:
            print('--prune-baseline needs a full run (no file arguments, no --lint-only).')
            return 2
        pruned = baseline - fixed
        write_baseline(pruned)
        print('Removed %d fixed entries from the baseline (%d remain).'
              % (sum(fixed.values()), sum(pruned.values())))

    for f in findings:
        if not f.known or args.show_known:
            print(('  ' if f.known else '') + str(f))

    def count(sev, known):
        return sum(1 for f in findings if f.severity == sev and f.known == known)

    print()
    print('Errors:   %d new, %d known' % (count('error', False), count('error', True)))
    print('Warnings: %d new, %d known' % (count('warning', False), count('warning', True)))
    if not partial and not args.prune_baseline and fixed:
        print('Fixed:    %d baseline entries no longer occur; run with --prune-baseline.'
              % sum(fixed.values()))
    if not os.path.isfile(BASELINE):
        print('No baseline file (%s); every finding counts as new.' % rel(BASELINE))

    if new:
        print('RESULT: FAIL (%d findings not in the baseline)' % len(new))
        return 1
    print('RESULT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
