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
        if args.output:
            try:
                output = open(args.output, 'w')
            except Exception:
                output.close()
        else:
            output = sys.stdout
        compile(source, output)
        output.close()
