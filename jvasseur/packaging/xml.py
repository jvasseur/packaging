import io, typing, xml.dom, xml.dom.minidom

from .feed import Archive, Command, FeedFor, Group, Implementation, Interface, ManifestDigest, Name, Runner, Summary

def _from_node(node):
    match node.tagName:
        case 'archive':
            element = Archive(
                href=node.getAttribute('href'),
                size=node.getAttribute('size'),
                extract=node.getAttribute('extract') if node.hasAttribute('extract') else None,
                type=node.getAttribute('type') if node.hasAttribute('type') else None,
            )
        case 'command':
            element = Command(
                name=node.getAttribute('name'),
                path=node.getAttribute('path'),
            )
        case 'group':
            element = Group(
                arch=node.getAttribute('arch') if node.hasAttribute('arch') else None,
            )
        case 'implementation':
            element = Implementation(
                arch=node.getAttribute('arch') if node.hasAttribute('arch') else None,
                id=node.getAttribute('id'),
                released=node.getAttribute('released'),
                stability=node.getAttribute('stability') if node.hasAttribute('stability') else None,
                version=node.getAttribute('version'),
            )
        case 'interface':
            element = Interface(uri=node.getAttribute('uri'))
        case 'manifest-digest':
            element = ManifestDigest(sha256new=node.getAttribute('sha256new'))
        case 'name':
            element = Name(node.firstChild.data)
        case 'runner':
            element = Runner(
                interface=node.getAttribute('interface'),
                version=node.getAttribute('version') if node.hasAttribute('version') else None,
            )
        case 'summary':
            element = Summary(node.firstChild.data)
        case _:
            raise Exception(f'Unknown element: {node.tagName}')

    for childNode in node.childNodes:
        if childNode.nodeType == xml.dom.Node.ELEMENT_NODE:
            element.append(_from_node(childNode))

    return element

def from_xml(file: typing.IO) -> Interface:
    interface = _from_node(xml.dom.minidom.parse(file).documentElement)

    if not isinstance(interface, Interface):
        raise Exception('Invalid document element')

    return interface

def _to_node(element, document):
    match element:
        case Archive(href=href, size=size, extract=extract, type=type):
            node = document.createElement('archive')
            node.setAttribute('href', href)
            node.setAttribute('size', str(size))
            if extract is not None:
                node.setAttribute('extract', extract)
            if type is not None:
                node.setAttribute('type', type)

            return node
        case Command(name=name, path=path, children=children):
            node = document.createElement('command')
            node.setAttribute('name', name)
            node.setAttribute('path', path)

            for child in children:
                node.appendChild(_to_node(child, document))

            return node
        case FeedFor(interface=interface):
            node = document.createElement('feed-for')
            node.setAttribute('interface', interface)

            return node
        case Group(arch=arch, children=children):
            node = document.createElement('group')
            if arch is not None:
                node.setAttribute('arch', arch)

            for child in children:
                node.appendChild(_to_node(child, document))

            return node
        case Implementation(arch=arch, id=id, released=released, stability=stability, version=version, children=children):
            node = document.createElement('implementation')
            if arch is not None:
                node.setAttribute('arch', arch)
            node.setAttribute('id', id)
            node.setAttribute('released', released)
            if stability is not None:
                node.setAttribute('stability', stability)
            node.setAttribute('version', version)

            for child in children:
                node.appendChild(_to_node(child, document))

            return node
        case ManifestDigest(sha256new=sha256new):
            node = document.createElement('manifest-digest')
            node.setAttribute('sha256new', sha256new)

            return node
        case Name(content=content):
            node = document.createElement('name')
            node.appendChild(document.createTextNode(content))

            return node
        case Runner(interface=interface, version=version):
            node = document.createElement('runner')
            node.setAttribute('interface', interface)
            if version is not None:
                node.setAttribute('version', version)

            return node
        case Summary(content=content):
            node = document.createElement('summary')
            node.appendChild(document.createTextNode(content))

            return node
        case _:
            raise Exception('Unknow element type')

def to_xml(interface: Interface, indent: str ='\t', newl: str ='\n') -> typing.IO:
    xmlns = 'http://zero-install.sourceforge.net/2004/injector/interface'

    implementation = xml.dom.minidom.getDOMImplementation()
    document = implementation.createDocument(xmlns, 'interface', None)

    document.documentElement.setAttribute('xmlns', xmlns)
    document.documentElement.setAttribute('uri', interface.uri)

    for element in interface.children:
        document.documentElement.appendChild(_to_node(element, document))

    file = io.StringIO()
    file.write('<?xml version="1.0"?>\n')

    document.documentElement.writexml(file, addindent=indent, newl=newl)

    file.seek(0)

    return file
