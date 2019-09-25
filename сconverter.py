#!/usr/bin/env python3
import sys
import argparse

ERROR_EXCEPTION = 1
ERROR_FILE_MISSING = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4
ERROR_WRONG_EXTENSION = 5

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


def parse_filename(file):
    separator = file.rfind('.')
    if separator == -1:
        return (file, "")
    return (file[:separator], file[separator + 1:])


def main():
    args = parse_args()
    (file_name, extension) = parse_filename(args.file)
    if extension != "cs":
        print('File is not correct', file=sys.stderr)
        sys.exit(ERROR_WRONG_EXTENSION)
    f = open(args.file, 'r')
    try:
        content = f.read()
    except Exception as e:
        print('File is mising: "{}"'.format(e), file=sys.stderr)
        sys.exit(ERROR_FILE_MISSING)
    finally:
        f.close()
    print(xmldoc2xml.convert(content, file_name=file_name), file=sys.stderr)

if __name__ == "__main__":
    main()
