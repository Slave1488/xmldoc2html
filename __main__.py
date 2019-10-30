import reader
import lineLexer as llexer
import memberCompiler as mcompiler
from layout import Tag, Attribute, view
import mapCreator as mcreator


with open('content.txt') as f:
    lr = reader.get_line_reader(f)
    lts = llexer.get_tokens(lr)
    ms = mcompiler.compile(lts)
    mmap = mcreator.create(*ms)
