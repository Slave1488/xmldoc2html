import attributeCreator as acreate


def decorate_member(member):
    decor = []
    mcharacter = member.get_attr('name')._value[0]
    decor.append(acreate.create_class(mcharacter))
    return decor
