import os, posixpath, subprocess, tempfile, urllib.parse, urllib.request

class Download:
    def __init__(self, url):
        path = urllib.parse.urlsplit(url).path
        basename = posixpath.basename(path)

        self.url = url
        self.temporary_file = tempfile.NamedTemporaryFile(suffix=basename)

    def __enter__(self):
        file = self.temporary_file.__enter__()

        with urllib.request.urlopen(self.url) as response:
            file.write(response.read())

        return file

    def __exit__(self, exc_type, exc_value, traceback):
        self.temporary_file.__exit__(exc_type, exc_value, traceback)

def get_size(archive):
    return os.path.getsize(archive)

def get_digest(archive, extract = None):
    base_args = ['0install', 'digest', '--algorithm=sha256new']
    extract_args = [extract] if extract is not None else []

    output = subprocess.check_output(base_args + [archive] + extract_args, encoding='utf-8')

    return output.removeprefix('sha256new_').removesuffix('\n')
