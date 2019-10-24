from run import run
import parserLines
from layout import Tag, Attribute, view

with open('content.txt', 'r') as f:
    parserLines.hardcore_pareser(parserLines.simple_parse(f))
