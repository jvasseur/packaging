import io
import typing
from xml import dom
from xml.dom import minidom

class Archive:
    def __init__(self, *, href: str, size: int, extract: str = None, type: str = None):
        self.href = href
        self.size = size
        self.extract = extract
        self.type = type

    def as_node(self, document):
        node = document.createElement('archive')
        node.setAttribute('href', self.href)
        node.setAttribute('size', str(self.size))
        if self.extract is not None:
            node.setAttribute('extract', self.extract)
        if self.type is not None:
            node.setAttribute('type', self.type)

        return node

class Command:
    def __init__(self, *, name, path):
        self.name = name
        self.path = path

    def as_node(self, document):
        node = document.createElement('command')
        node.setAttribute('name', self.name)
        node.setAttribute('path', self.path)

        return node

class FeedFor:
    def __init__(self, *, interface):
        self.interface = interface

    def as_node(self, document):
        node = document.createElement('feed-for')
        node.setAttribute('interface', self.interface)

        return node

class Implementation:
    def __init__(self, *children, id, released, stability: str = None, version):
        self.children = children
        self.id = id
        self.released = released
        self.stability = stability
        self.version = version

    def as_node(self, document):
        node = document.createElement('implementation')
        node.setAttribute('id', self.id)
        node.setAttribute('released', self.released)
        if self.stability is not None:
            node.setAttribute('stability', self.stability)
        node.setAttribute('version', self.version)

        for element in self.children:
            node.appendChild(element.as_node(document))

        return node

class Interface:
    def __init__(self, *children):
        self.children = list(children)

    def append(self, element):
        self.children.append(element)

class ManifestDigest:
    def __init__(self, *, sha256new):
        self.sha256new = sha256new

    def as_node(self, document):
        node = document.createElement('manifest-digest')
        node.setAttribute('sha256new', self.sha256new)

        return node

class Group:
    def __init__(self, *children, arch):
        self.children = list(children)
        self.arch = arch

    def append(self, element):
        self.children.append(element)

    def as_node(self, document):
        node = document.createElement('group')
        node.setAttribute('arch', self.arch)

        for element in self.children:
            node.appendChild(element.as_node(document))

        return node

class Name:
    def __init__(self, content):
        self.content = content

    def as_node(self, document):
        node = document.createElement('name')
        node.appendChild(document.createTextNode(self.content))

        return node

class Summary:
    def __init__(self, content):
        self.content = content

    def as_node(self, document):
        node = document.createElement('summary')
        node.appendChild(document.createTextNode(self.content))

        return node

def _from_node(node):
    match node.tagName:
        case 'group':
            element = Group(
                arch=node.getAttribute('arch'),
            )
        case 'implementation':
            element = Implementation(
                id=node.getAttribute('id'),
                released=node.getAttribute('released'),
                stability=node.getAttribute('stability') if node.hasAttribute('stability') else None,
                version=node.getAttribute('version'),
            )
        case 'interface':
            element = Interface()
        case _:
            raise Exception(f'Unknown element: {node.tagName}')

    for childNode in node.childNodes:
        if childNode.nodeType == dom.Node.ELEMENT_NODE:
            element.append(_from_node(childNode))

    return element

def from_xml(file: typing.IO) -> Interface:
    interface = _from_node(minidom.parse(file).documentElement)

    if not isinstance(interface, Interface):
        raise Exception('Invalid document element')

    return interface

def _to_node(element, document):
    element.as_node(document)

def to_xml(interface: Interface, indent: str ='\t', newl: str ='\n') -> typing.IO:
    xmlns = 'http://zero-install.sourceforge.net/2004/injector/interface'

    implementation = minidom.getDOMImplementation()
    document = implementation.createDocument(xmlns, 'interface', None)

    document.documentElement.setAttribute('xmlns', xmlns)

    for element in interface.children:
        document.documentElement.appendChild(_to_node(element, document))

    file = io.StringIO()
    file.write('<?xml version="1.0"?>\n')

    document.documentElement.writexml(file, addindent=indent, newl=newl)

    file.seek(0)

    return file
