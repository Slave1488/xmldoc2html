from ..markup.markup import *


def convert(content, **kwargs):
    def make_member():
        pass
    doc = markup()
    tag_doc = tag("doc")
    doc.add_tag(tag_doc)
    assembly = tag("assembly")
    tag_doc.add_tag(assembly)
    if ("file_name" in kwargs):
        assembly_name = tag("name")
        assembly.add_tag(assembly_name)
        assembly_name.add_content(kwargs["file_name"])
    members = tag("members")
    tag_doc.add_tag(members)
    return str(doc)
