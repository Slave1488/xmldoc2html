from layout import Tag, Attribute
from memberID import Character
import attributeCreator as acreate

member_stylesheet = Tag('style')
with open('member_style.css') as style:
    member_stylesheet.add_content(style.read())


def decorate_member(member):
    decor = []
    mcharacter = member.get_attr('name')._value[0]
    decor.append(acreate.create_class(mcharacter))
    return decor
