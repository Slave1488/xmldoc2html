from layout import Page, view
import reader
import fileNameParser as nparser
import lineLexer as llexer
import memberCompiler as mcompiler
import mapCreator as mcreator
import tableCompile as tcompile
from tagDecorator import decorate_member
import styleCreator as screator


def save_gen(generator):
    return list(generator)


def compile(source, output):
    page = Page()
    lines = reader.get_line_reader(source)
    lts = llexer.get_tokens(lines)
    members = mcompiler.compile(lts)
    members = save_gen(members)
    member_map = mcreator.create(*members)
    table = tcompile.compile(
        member_map, members,
        caption=nparser.parse(source.name),
        decorate=decorate_member)
    styles = []
    with open('member_style.css') as ms:
        styles.append(screator.create(ms))
    with open('table_style.css') as ts:
        styles.append(screator.create(ts))
    page.add_content(*styles, table)
    output.write(page.view())
