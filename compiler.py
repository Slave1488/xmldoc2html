import os
from pathlib import Path
from layout.description import Page, view
from layout.map import creator as mcreator
from layout.decorator import decorate_member
from filesup import reader, nameparser as nparser
from cscode import linelexer as llexer
from myxml.member import compiler as mcompiler
from htmlsup import tablecompile as tcompile, stylecreator as screator


def save_gen(generator):
    return list(generator)


def compile(source):
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
    styles_dir = Path(os.path.dirname(__file__), 'htmlsup', 'styles')
    with open(styles_dir / 'member_style.css') as ms:
        styles.append(screator.create(ms))
    with open(styles_dir / 'table_style.css') as ts:
        styles.append(screator.create(ts))
    page.add_content(*styles, table)
    return page.view()
