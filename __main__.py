from layout import Page, view
import reader
import lineLexer as llexer
import memberCompiler as mcompiler
import mapCreator as mcreator
import tableCompile as tcompile
from tagDecorator import decorate_member
import styleCreator as screator


def save(generator):
    return list(generator)


def main():
    page = Page()
    with open('content.txt') as f:
        lines = reader.get_line_reader(f)
        lts = llexer.get_tokens(lines)
        members = mcompiler.compile(lts)
        members = save(members)
    member_map = mcreator.create(*members)
    table = tcompile.compile(
        member_map, members, caption=f.name,
        decorate=decorate_member)
    styles = []
    with open('member_style.css') as ms:
        styles.append(screator.create(ms))
    with open('table_style.css') as ts:
        styles.append(screator.create(ts))
    page.add_content(*styles, table)
    with open('html.html', 'w') as html:
        html.write(page.view())


if __name__ == '__main__':
    main()
