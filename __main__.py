import reader
import lineLexer as llexer
import memberCompiler as mcompiler
from layout import Tag, Attribute, view
import mapCreator as mcreator
import tableCompile as tcompile


with open('content.txt') as f, open('html.html', 'w') as html:
    lr = reader.get_line_reader(f)
    lts = llexer.get_tokens(lr)
    ms = list(mcompiler.compile(lts))
    mmap = mcreator.create(*ms)
    table = tcompile.compile(mmap, ms, f.name)
    html.write(view(table))
