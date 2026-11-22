"""Download the external schemas PIXM imports into .schema-cache/.

Usage:
    python tools/fetch_schemas.py            # fetch anything missing
    python tools/fetch_schemas.py --refresh  # re-download everything
"""

import argparse
import sys

import schema_cache


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--refresh', action='store_true',
                        help='re-download schemas that are already cached')
    args = parser.parse_args()

    print('Fetching external schemas into %s' % schema_cache.CACHE_DIR)
    downloaded, cached, failures = schema_cache.fetch(refresh=args.refresh)
    print('Downloaded %d, already cached %d, failed %d.' % (downloaded, cached, len(failures)))
    for url, msg in failures:
        print('  FAILED %s: %s' % (url, msg))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
