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

    def version(self, tag_name):
        return tag_name.removeprefix('v')

    @abc.abstractmethod
    def assets(self, assets):
        pass

    @abc.abstractmethod
    def manifest_digest(self, data):
        pass

    @abc.abstractmethod
    def retrieval(self, data):
        pass

    @abc.abstractmethod
    def commands(self, data):
        pass

    def implementations(self):
        releases = json.loads(urllib.request.urlopen(f'https://api.github.com/repos/{self.repo}/releases').read())

        for release in reversed(releases):
            version = self.version(release['tag_name'])

            if version is not None:
                for arch, asset in self.assets(release['assets']):
                    yield version if arch is None else f'{version}-{arch}', {
                        'arch': arch,
                        'asset': asset,
                        'release': release,
                        'version': version,
                    }

    def implementation(self, data):
        return Implementation(
            ManifestDigest(sha256new=self.manifest_digest(data)),
            self.retrieval(data),
            *self.commands(data),
            arch=data['arch'],
            id=data['version'] if data['arch'] is None else f'{data['version']}-{data['arch']}',
            version=data['version'],
            released=data['release']['published_at'][0:10],
            stability='testing' if data['release']['prerelease'] else 'stable',
        )

class ArchiveGitHubApp(GitHubApp):
    def extract(self, data):
        return None

    def manifest_digest(self, data):
        extract = self.extract(data)

        with Download(data['asset']['browser_download_url']) as archive:
            return get_digest(archive.name, extract)

    def retrieval(self, data):
        return Archive(
            href=data['asset']['browser_download_url'],
            size=data['asset']['size'],
            extract=self.extract(data),
        )

class FileGitHubApp(GitHubApp):
    def file_name(self, data):
        return posixpath.basename(urllib.parse.urlsplit(data['asset']['browser_download_url']).path)

    def file_executable(self, data):
        return True

    def manifest_digest(self, data):
        if data['asset']['digest'] is not None and data['asset']['digest'].startswith('sha256:'):
            sha256 = data['asset']['digest'].removeprefix('sha256:')
        else:
            with Download(data['asset']['browser_download_url']) as file:
                sha256 = hashlib.file_digest(file, 'sha256').hexdigest()

        return get_manifest_digest([
            ManifestFile(
                executable=self.file_executable(data),
                mtime=0,
                name=self.file_name(data),
                sha256=sha256,
                size=data['asset']['size'],
            ),
        ], 'sha256new')

    def retrieval(self, data):
        return File(
            href=data['asset']['browser_download_url'],
            size=data['asset']['size'],
            dest=self.file_name(data),
            executable=self.file_executable(data),
        )

    def commands(self, data):
        yield Command(name='run', path=self.file_name(data))
