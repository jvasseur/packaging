import abc, hashlib, json, posixpath, urllib.parse, urllib.request

from ..feed import Archive, Command, File, Implementation, ManifestDigest
from ..manifest import get_manifest_digest, ManifestFile
from .utils import Download, get_digest, get_size
from . import App

class GitHubApp(App):
    @property
    @abc.abstractmethod
    def repo():
        pass

    @abc.abstractmethod
    def assets(self, assets):
        pass

    def version(self, tag_name):
        return tag_name.removeprefix('v')

    def implementations(self):
        releases = json.loads(urllib.request.urlopen(f'https://api.github.com/repos/{self.repo}/releases').read())

        for release in reversed(releases):
            version = self.version(release['tag_name'])

            if version is not None:
                for arch, asset in self.assets(release['assets']):
                    yield f'{version}-{arch}', {
                        'arch': arch,
                        'asset': asset,
                        'release': release,
                        'version': version,
                    }

class ArchiveGitHubApp(GitHubApp):
    @abc.abstractmethod
    def commands(self, data):
        pass

    def extract(self, data):
        return None

    def implementation(self, data):
        extract = self.extract(data)

        with Download(data['asset']['browser_download_url']) as archive:
            digest = get_digest(archive.name, extract)

        return Implementation(
            ManifestDigest(sha256new=digest),
            Archive(
                href=data['asset']['browser_download_url'],
                size=data['asset']['size'],
                extract=extract,
            ),
            *self.commands(data),
            arch=data['arch'],
            id=f'{data['version']}-{data['arch']}',
            version=data['version'],
            released=data['release']['published_at'][0:10],
            stability='testing' if data['release']['prerelease'] else 'stable',
        )

class FileGitHubApp(GitHubApp):
    def file_name(self, data):
        return posixpath.basename(urllib.parse.urlsplit(data['asset']['browser_download_url']).path)

    def implementation(self, data):
        file_name = self.file_name(data)

        if data['asset']['digest'] is not None and data['asset']['digest'].startswith('sha256:'):
            sha256 = data['asset']['digest'].removeprefix('sha256:')
        else:
            with Download(data['asset']['browser_download_url']) as file:
                sha256 = hashlib.file_digest(file, 'sha256').hexdigest()

        digest = get_manifest_digest([
            ManifestFile(
                executable=True,
                mtime= 0,
                name=file_name,
                sha256=sha256,
                size=data['asset']['size'],
            ),
        ], 'sha256new')

        return Implementation(
            ManifestDigest(sha256new=digest),
            File(
                href=data['asset']['browser_download_url'],
                size=data['asset']['size'],
                dest=file_name,
                executable=True,
            ),
            Command(
                name='run',
                path=file_name,
            ),
            arch=data['arch'],
            id=f'{data['version']}-{data['arch']}',
            version=data['version'],
            released=data['release']['published_at'][0:10],
            stability='testing' if data['release']['prerelease'] else 'stable',
        )
