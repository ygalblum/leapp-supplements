import os
import re
import requests


class Downloader(object):

    @classmethod
    def download(cls, url, target_dir, default_filename):
        r = requests.get(url, allow_redirects=True, timeout=10)
        filename = cls._get_filename_from_cd(r.headers, default_filename)
        file_path = os.path.join(target_dir, filename)
        with open(file_path, "wb") as f:
            f.write(r.content)
        return file_path

    @staticmethod
    def _get_filename_from_cd(headers, default_filename):
        cd = headers.get('content-disposition')
        if cd:
            fname = re.findall('filename=(.+)', cd)
            if fname:
                return fname[0]
        return default_filename

    @staticmethod
    def get(url):
        r = requests.get(url, allow_redirects=True, timeout=10)
        r.raise_for_status()
        return r.content
