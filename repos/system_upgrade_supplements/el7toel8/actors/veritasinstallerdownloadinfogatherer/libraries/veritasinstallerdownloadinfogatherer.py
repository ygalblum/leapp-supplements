import json
import six.moves.urllib.parse as urlparse

from leapp.models import VeritasInstallerDownloadInfo, VeritasInstallerPatchDownloadInfo


def process(json_file, downloader):
    if urlparse.urlparse(json_file).scheme != "":
        info = downloader.get(json_file)
    else:
        with open(json_file, "r") as f:
            info = json.load(f)

    return VeritasInstallerDownloadInfo(
        installer_tar_url=info['ga_installer'],
        install_response_file_url=info['install_response'],
        uninstall_response_file_url=info['uninstall_response'],
        patches=[
            VeritasInstallerPatchDownloadInfo(url=p['url'], response_file=p['response_file']) for p in info['patches']
        ],
    )
