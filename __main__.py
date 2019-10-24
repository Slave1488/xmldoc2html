from run import run
import parserLines
from layout import Tag, Attribute, view

with open('content.txt', 'r') as f:
    for part in parserLines.get_simple_parser(f):
        print(view(part))

html = Tag('html')
html.add_attribute(Attribute('name', 'legion'))
body = Tag('body')
html.add_content(Tag('head'))
html.add_content(body)
body.add_content('text')
print(view(html))
