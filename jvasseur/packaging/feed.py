class Archive:
    def __init__(self, *, href: str, size: int, extract: str = None, type: str = None):
        self.href = href
        self.size = size
        self.extract = extract
        self.type = type

    def __eq__(self, other):
        return self.href == other.href and self.size == other.size and self.extract == other.extract and self.type == other.type

class Arg:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content

class Category:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content

class Command:
    def __init__(self, *children, name, path):
        self.children = list(children)
        self.name = name
        self.path = path

    def __eq__(self, other):
        return self.name == other.name and self.path == other.path and self.children == other.children

    def append(self, element):
        self.children.append(element)

class Description:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content

class Environment:
    def __init__(self, *, name: str, insert: str = None, value: str = None, mode: str = None, separator: str = None, default: str = None):
        self.name = name
        self.insert = insert
        self.value = value
        self.mode = mode
        self.separator = separator
        self.default = default

    def __eq__(self, other):
        return self.name == other.name and self.insert == other.insert and self.value == other.value and self.mode == other.mode and self.separator == other.separator and self.default == other.default

class FeedFor:
    def __init__(self, *, interface):
        self.interface = interface

class ForEach:
    def __init__(self, *children, item_from: str, separator: str = None):
        self.children = list(children)
        self.item_from = item_from
        self.separator = separator

    def __eq__(self, other):
        return self.item_from == other.item_from and self.separator == other.separator and self.children == other.children

    def append(self, element):
        self.children.append(element)

class File:
    def __init__(self, *, href: str, size: int, dest: str, executable: bool = None):
        self.href = href
        self.size = size
        self.dest = dest
        self.executable = executable

class Group:
    def __init__(self, *children, arch = None, released = None, stability = None, version = None):
        self.children = list(children)
        self.arch = arch
        self.released = released
        self.stability = stability
        self.version = version

    def append(self, element):
        self.children.append(element)

    def get_commands(self):
        return [child for child in self.children if isinstance(child, Command)]

    def implementations(self):
        children = []
        implementations = []

        for child in self.children:
            if isinstance(child, Group):
                implementations.extend(child.implementations())
            elif isinstance(child, Implementation):
                implementations.append(child)
            else:
                children.append(child)

        for implementation in implementations:
            yield Implementation(
                [*children, implementation.children],
                arch=implementation.arch if implementation.arch is not None else self.arch,
                id=implementation.id,
                released=implementation.released if implementation.released is not None else self.released,
                stability=implementation.stability if implementation.stability is not None else self.stability,
                version=implementation.version if implementation.version is not None else self.version,
            )

class Homepage:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content

class Icon:
    def __init__(self, *, href: str, type: str):
        self.href = href
        self.type = type

    def __eq__(self, other):
        return self.href == other.href and self.type == other.type

class Implementation:
    def __init__(self, *children, arch = None, id, released, stability: str = None, version):
        self.children = list(children)
        self.arch = arch
        self.id = id
        self.released = released
        self.stability = stability
        self.version = version

    def __eq__(self, other):
        return self.arch == other.arch and self.id == other.id and self.released == other.released and self.stability == other.stability and self.version == other.version and self.children == other.children

    def append(self, element):
        self.children.append(element)

    def get_commands(self):
        return [child for child in self.children if isinstance(child, Command)]

class Interface:
    def __init__(self, *children, uri):
        self.uri = uri
        self.children = list(children)

    def __eq__(self, other):
        return self.uri == other.uri and self.children == other.children

    def append(self, element):
        self.children.append(element)

    def implementations(self):
        for child in self.children:
            if isinstance(child, Implementation):
                yield child
            if isinstance(child, Group):
                yield from child.implementations()

class ManifestDigest:
    def __init__(self, *, sha256new):
        self.sha256new = sha256new

class Name:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content

class Publisher:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content

class Runner:
    def __init__(self, *, interface, version = None):
        self.interface = interface
        self.version = version

    def __eq__(self, other):
        return self.interface == other.interface and self.version == other.version

class SplashScreen:
    def __init__(self, *, href: str, type: str):
        self.href = href
        self.type = type

    def __eq__(self, other):
        return self.href == other.href and self.type == other.type

class Summary:
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return self.content == other.content
