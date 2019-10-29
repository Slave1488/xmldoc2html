import reader
import lineLexer as llexer
import memberCompiler as mcompiler
from layout import Tag, Attribute, view


with open('content.txt') as f:
    lr = reader.get_line_reader(f)
    lts = llexer.get_tokens(lr)
    ms = mcompiler.compile(lts)
    for member in ms:
        print(view(member))
