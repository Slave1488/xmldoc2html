from layout.description import Tag


def create(file):
    style = Tag('style')
    style.add_content(file.read())
    return style
