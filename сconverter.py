#!/usr/bin/env python3
import sys
import argparse

ERROR_EXCEPTION = 1
ERROR_FILE_MISSING = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4

if sys.version_info < (3, 6):
    print('Use python >= 3.6', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

if sys.platform.startswith('linux'):
    import readline

try:
    from convert import xmldoc2xml
except Exception as e:
    print('Convert modules not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                        action="store",
                        type=str,
                        help="file to convert",
                        metavar="file")
    return parser.parse_args()


def main():
    args = parse_args()
    print(args.file)
    try:
        f = open(args.file, 'r')
    except Exception as e:
        print('File not found: "{}"'.format(e), file=sys.stderr)
        sys.exit(ERROR_FILE_MISSING)
    else:
        content = f.read()
    finally:
        f.close()
    print(xmldoc2xml.convert(content), file=sys.stderr)

if __name__ == "__main__":
    main()
