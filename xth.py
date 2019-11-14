#!/usr/bin/env python3

import sys
import argparse
from compiler import compile

description = '''
Compiles C# source code into HTML documentation'''
parser = argparse.ArgumentParser(description=description)

source_help = '''
source code in c#'''
parser.add_argument(
    'source', help=source_help)

output_help = '''
output file'''
parser.add_argument(
    '--out', help=output_help,
    metavar='file', dest='output')

if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.source) as source:
        with open(args.output, 'w') if args.output else sys.stdout as output:
            doc = compile(source)
            output.write(doc)
        output.close()
