import sys
import argparse
from compiler import compile

parser = argparse.ArgumentParser()

parser.add_argument('source')

parser.add_argument(
    '--out', metavar='file', dest='output')

if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.source) as source:
        with open(args.output, 'w') if args.output else sys.stdout as output:
            compile(source, output)
        output.close()
