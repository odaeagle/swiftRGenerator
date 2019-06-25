import xml.etree.ElementTree as ET
from xml.etree import ElementTree

INPUT_NAME = 'strings.xml'

# Custom builder so parser will not ignore all comments
class CommentedTreeBuilder(ElementTree.TreeBuilder):
    def __init__(self, *args, **kwargs):
        super(CommentedTreeBuilder, self).__init__(*args, **kwargs)

    def comment(self, data):
        self.start(ElementTree.Comment, {})
        self.data(data)
        self.end(ElementTree.Comment)

# Code Generation Template
template = """
    static var {} = {{
        return EDLocalizedString("{}", comment: "{}")
    }}
    """

def process(file: str):
    parser = ET.XMLParser(target = CommentedTreeBuilder())
    tree = ET.parse('strings.xml', parser=parser)
    root = tree.getroot()
    
    f = open('ios.strings', 'w')
    f2 = open('R.swift', 'w')
    
    f2.write('class R {\n')
    
    for child in root:
        print(child.tag)
        if callable(child.tag):
            # it's a comment
            continue
        if child.tag == 'string':
            key = child.attrib['name']
            value = child.text
            f.write('"{}" = "{}";\n'.format(key, value))
            f2.write(template.format(key, key, value))
    f.close()
    
    f2.write('}\n')
    f2.close()    

process(INPUT_NAME)
