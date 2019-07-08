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


def clean_name(name: str) -> str:
    words = name.strip().split('_')
    words = list(map(lambda x: x[0].upper() + x[1:], words))
    words[0] = words[0][0].lower() + words[0][1:]
    return ''.join(words)


class PluralsEntry:

    key: str


class Entry:
    
    key: str
    value: str
    has_arg: bool
    args: [(str, str)]
    
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        self.args = []
        self._process()
        
    def _process(self):
        if '%' in self.value:
            # with arg
            self.has_arg = True
            index = 0
            arg_count = 0
            while True:
                found = self.value.find('%', index)
                if found == -1:
                    break
                arg_count += 1
                placeholder = self.value[index: index + 2]
                if placeholder == '%d':
                    self.args.append(('arg' + str(arg_count),\
                                      'Int'))
                elif placeholder == '%s':
                    self.value = self.value[:index] + '%@' + self.value[index + 2:]
                    self.args.append(('arg' + str(arg_count),\
                                      'String'))
                elif placeholder == '%f':
                    self.args.append(('arg' + str(arg_count),\
                                      'Float'))
                index = found + 1
                
        else:
            # without arg
            self.has_arg = False
        
    def __repr__(self):
        return '<{}, {} {}>'.format(self.key, self.value, self.args)
    

# Code Generation Template
template_no_arg = """
    static var {} = {{
        return EDLocalizedString("{}", comment: "{}")
    }}
    """
template_with_arg = """
    static func {}({}) {{
        return EDLocalizedString("{}", comment: "{}")
    }}
    """


def process(file: str):
    result = {}
    parser = ET.XMLParser(target=CommentedTreeBuilder())
    tree = ET.parse('strings.xml', parser=parser)
    root = tree.getroot()

    curr_section = None
    for child in root:
        print("TAG", child.tag)
        if callable(child.tag):
            section_name = clean_name(child.text)
            curr_section = section_name
            result[curr_section] = []
        elif child.tag == 'string':
            key = child.attrib['name']
            value = child.text
            entry = Entry(key, value)
            result[curr_section].append(entry)
        elif child.tag == 'plurals':
            print(dir(child))
            for element in child:
                key = element.attrib['quantity']
                value = element.text
                print(key, value)
            print(list(child))
    print(result)


if __name__ == '__main__':
    process(INPUT_NAME)
