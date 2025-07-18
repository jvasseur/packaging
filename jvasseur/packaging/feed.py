class Archive:
    def __init__(self, *, href: str, size: int, extract: str = None, type: str = None):
        self.href = href
        self.size = size
        self.extract = extract
        self.type = type

class Command:
    def __init__(self, *children, name, path):
        self.children = list(children)
        self.name = name
        self.path = path

    def __eq__(self, other):
        return self.name == other.name and self.path == other.path and self.children == other.children

    def append(self, element):
        self.children.append(element)

class FeedFor:
    def __init__(self, *, interface):
        self.interface = interface

class Implementation:
    def __init__(self, *children, arch = None, id, released, stability: str = None, version):
        self.children = list(children)
        self.arch = arch
        self.id = id
        self.released = released
        self.stability = stability
        self.version = version

    def append(self, element):
        self.children.append(element)

    def get_commands(self):
        return [child for child in self.children if isinstance(child, Command)]

class Interface:
    def __init__(self, *children):
        self.children = list(children)

    def implementations(self):
        for child in self.children:
            if isinstance(child, Implementation):
                yield child
            if isinstance(child, Group):
                yield from child.implementations()

    def append(self, element):
        self.children.append(element)

class ManifestDigest:
    def __init__(self, *, sha256new):
        self.sha256new = sha256new

class Name:
    def __init__(self, content):
        self.content = content

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

class Runner:
    def __init__(self, *, interface, version = None):
        self.interface = interface
        self.version = version

    def __eq__(self, other):
        return self.interface == other.interface and self.version == other.version

class Summary:
    def __init__(self, content):
        self.content = content
