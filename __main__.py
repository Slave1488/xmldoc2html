import reader
import lineLexer as llexer
import memberCompiler as mcompiler
from layout import Page, view
import mapCreator as mcreator
import tableCompile as tcompile
from tagDecorator import decorate_member
import styleCreator as screator


def main():
    with open('content.txt') as f, open('html.html', 'w') as html:
        lines = reader.get_line_reader(f)
        lts = llexer.get_tokens(lines)
        members = mcompiler.compile(lts)
        member_map = mcreator.create(*members)
        table = tcompile.compile(
            member_map, members, caption=f.name,
            decorate=decorate_member)
        page = Page()
        styles = []
        with open('member_style.css') as ms, open('table_style.css') as ts:
            styles.append(screator.create(ms))
            styles.append(screator.create(ts))
        page.add_content(*styles, table)
        html.write(page.view())


if __name__ == '__main__':
    main()
