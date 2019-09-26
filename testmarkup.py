from markup.markup import *

doc = markup()

html = tag("html")
head = tag("head")
title = tag("title")
body = tag("body")
body.add_attribute(attribute("id", "13_54"))

html.add_tag(head)
html.add_tag(body)
head.add_tag(title)
title.add_content("BIG TITLE")

doc.add_tag(html)

print(str(doc))
