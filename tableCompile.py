from layout import Tag


def compile_line(content_list):
    tr = Tag('tr')
    for cont in content_list:
        td = Tag('td')
        td.add_content(*cont)
        tr.add_content(td)
    return tr


def compile(xmap, xml_tags, caption=None):
    table = Tag('table')
    if caption:
        cap_cont = caption
        caption = Tag('caption')
        caption.add_content(cap_cont)
        table.add_content(caption)
    for xtag in xml_tags:
        table.add_content(compile_line(xmap.get_content(xtag)))
    return table
