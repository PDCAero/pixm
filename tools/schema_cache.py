"""Local cache of external schemas (GML, ISO 19139, AIXM, ...).

Published PIXM schemas reference external schemas by their official online
URLs. For fast, offline validation those files are mirrored into
`.schema-cache/` (git-ignored), keeping each URL's host and path, so relative
imports inside the external schemas still resolve.

Downloads verify TLS certificates using the `certifi` trust store, which is
more up to date than some system Python stores.
"""

import os
import ssl
import urllib.parse
import urllib.request
from collections import deque

from lxml import etree

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(REPO_ROOT, '.schema-cache')
SCHEMA_DIR = os.path.join(REPO_ROOT, 'schema', '0.5')

XS = 'http://www.w3.org/2001/XMLSchema'
USER_AGENT = 'pixm-schema-fetch/1.0'


def is_remote(url):
    return url.startswith(('http://', 'https://'))


def cache_path(url):
    """Local cache file for a remote URL (scheme is ignored)."""
    parts = urllib.parse.urlsplit(url)
    path = parts.path.lstrip('/') or 'index.xsd'
    return os.path.join(CACHE_DIR, parts.netloc.lower(), *path.split('/'))


def uri_mapper(url):
    """Map a remote URL to its cached copy when present; otherwise unchanged."""
    if is_remote(url):
        local = cache_path(url)
        if os.path.isfile(local):
            return local
    return url


def _ssl_context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def _download(url, ctx):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        return resp.read()


def _schema_refs(data):
    """schemaLocation values of xs:import / xs:include / xs:redefine."""
    root = etree.fromstring(data)
    refs = []
    for tag in ('import', 'include', 'redefine'):
        for el in root.iter('{%s}%s' % (XS, tag)):
            loc = el.get('schemaLocation')
            if loc:
                refs.append(loc)
    return refs


def pixm_remote_imports():
    """Remote schemaLocations referenced directly by the PIXM schema files."""
    urls = []
    for name in sorted(os.listdir(SCHEMA_DIR)):
        if name.endswith('.xsd'):
            with open(os.path.join(SCHEMA_DIR, name), 'rb') as f:
                urls += [u for u in _schema_refs(f.read()) if is_remote(u)]
    return sorted(set(urls))


def fetch(refresh=False, log=print):
    """Download all remote schemas reachable from the PIXM schema files.

    Returns (downloaded, cached, failures) where failures is a list of
    (url, error message).
    """
    ctx = _ssl_context()
    queue = deque(pixm_remote_imports())
    seen = set()
    downloaded = cached = 0
    failures = []
    while queue:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        local = cache_path(url)
        if os.path.isfile(local) and not refresh:
            with open(local, 'rb') as f:
                data = f.read()
            cached += 1
        else:
            try:
                data = _download(url, ctx)
            except Exception as exc:  # report and continue with the rest
                failures.append((url, str(exc)))
                continue
            os.makedirs(os.path.dirname(local), exist_ok=True)
            with open(local, 'wb') as f:
                f.write(data)
            downloaded += 1
            log('  fetched %s' % url)
        try:
            refs = _schema_refs(data)
        except etree.XMLSyntaxError as exc:
            failures.append((url, 'not well-formed: %s' % exc))
            continue
        for ref in refs:
            queue.append(urllib.parse.urljoin(url, ref))
    return downloaded, cached, failures


def cache_present():
    return all(os.path.isfile(cache_path(u)) for u in pixm_remote_imports())
