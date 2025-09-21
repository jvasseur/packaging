import base64, hashlib

class ManifestFile:
    def __init__(self, *, executable = False, mtime, name, sha256 = None, size):
        self.executable = executable
        self.mtime = mtime
        self.name = name
        self.sha256 = sha256
        self.size = size
        pass

    def _manifest(self, alg):
        hash = None

        if alg == 'sha256' or alg == 'sha256new':
            hash = self.sha256

        if hash is None:
            raise 'Missing hash'

        return f'{'X' if self.executable else 'F'} {hash} {self.mtime} {self.size} {self.name}\n'

def get_manifest(content, alg) -> str:
    return ''.join(map(lambda element: element._manifest(alg), content))

def get_manifest_digest(content, alg) -> str:
    if alg == 'sha256' or alg == 'sha256new':
        hash = hashlib.sha256(get_manifest(content, alg).encode())

        if alg == 'sha256':
            return hash.hexdigest()

        if alg == 'sha256new':
            return base64.b32encode(hash.digest()).decode().rstrip('=')
