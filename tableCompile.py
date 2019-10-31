from layout import Tag


def compile_th_tr(name_list):
    tr = Tag('tr')
    for cont in name_list:
        td = Tag('td')
        td.add_content(*cont)
        tr.add_content(td)
    return tr


def compile_tr(content_list):
    tr = Tag('tr')
    for cont in content_list:
        td = Tag('td')
        td.add_content(*cont)
        tr.add_content(td)
    return tr


def compile(xmap, xml_tags, *, caption=None, decorate=None):
    table = Tag('table')
    if caption:
        cap_cont = caption
        caption = Tag('caption')
        caption.add_content(cap_cont)
        table.add_content(caption)
    tr_th = compile_th_tr(xmap.get_names(main='member'))
    table.add_content(tr_th)
    for xtag in xml_tags:
        tr = compile_tr(xmap.get_content(xtag))
        if decorate:
            tr.add_attrs(*decorate(xtag))
        table.add_content(tr)
    return table
