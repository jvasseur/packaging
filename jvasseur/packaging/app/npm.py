import abc, json, re, urllib.request

from ..feed import Archive, Command, Implementation, ManifestDigest, Runner
from .utils import Download, get_digest, get_size
from . import App

def convert_version_range(range):
    if range.startswith('>='):
        return f'{range[2:]}..'

    if range.startswith('^'):
        version = list(map(int, range[1:].split('.')))

        return f'{range[1:]}..!{version[0] + 1}'

    return range

def convert_version_constraint(constraint):
    return ' | '.join(map(lambda range: convert_version_range(range.strip()), re.split('\\|\\|?', constraint)))

def create_node_command(name, path, constraint = None):
    return Command(
        Runner(
            interface='https://apps.0install.net/javascript/node.xml',
            version=convert_version_constraint(constraint) if constraint is not None else None,
        ),
        name=name,
        path=path,
    )

class NpmApp(App):
    @property
    @abc.abstractmethod
    def name():
        pass

    def implementations(self):
        data = json.loads(urllib.request.urlopen(f'https://registry.npmjs.org/{self.name}').read())

        for version, version_data in data['versions'].items():
            yield version, {
                **version_data,
                'time': data['time'][version],
            }

    def implementation(self, data):
        with Download(data['dist']['tarball']) as archive:
            size = get_size(archive.name)
            digest = get_digest(archive.name, 'package')

        return Implementation(
            ManifestDigest(sha256new=digest),
            Archive(
                href=data['dist']['tarball'],
                extract='package',
                size=size,
            ),
            *self.commands(data),
            id=data['version'],
            version=data['version'],
            released=data['time'][0:10],
        )

    def commands(self, data):
        constraint = data.get('engines', {}).get('node')

        if isinstance(data['bin'], dict):
            return [create_node_command('run' if name == self.name else name, path, constraint) for name, path in data['bin'].items()]

        if isinstance(data['bin'], str):
            return [create_node_command('run', data['bin'], constraint)]

        return []
