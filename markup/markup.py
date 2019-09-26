from functools import reduce


class content:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return content


class attribute:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return ' {name}="{value}"'.format(
            name=self.name,
            value=self.value
        )


class tag:
    def __init__(self, name):
        self.name = name
        self.attributs = []
        self.attachments = []

    def add_attribute(self, attribute):
        self.attributs.append(attribute)

    def add_tag(self, tag):
        self.attachments.append(tag)

    def add_content(self, content):
        self.attachments.append(content)

    def __str__(self):
        def reducer_attachments(a, n):
            return "{}\t{}\n".format(a, str(n).replace('\n', '\n\t'))
        return "<{name}{attributs}>\n{attachments}</{name}>".format(
            name=self.name,
            attributs=reduce(lambda a, n: a + str(n), self.attributs, ""),
            attachments=reduce(reducer_attachments, self.attachments, "")
        )


class markup:
    def __init__(self):
        self.attachments = []

    def add_tag(self, tag):
        self.attachments.append(tag)

    def add_content(self, content):
        self.attachments.append(content)

    def __str__(self):
        return reduce(lambda a, n: "{}{}\n".format(a, n), self.attachments, "")
