class content:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return content


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


class markup:
    def __init__(self):
        self.attachments = []

    def add_tag(self, tag):
        self.attachments.append(tag)

    def add_content(self, content):
        self.attachments.append(content)
