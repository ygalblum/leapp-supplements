import os

from leapp.exceptions import StopActorExecution
from leapp.libraries.common import veritas
from leapp.models import VeritasInstallerInfo

_DEAFULT_DOWNLOAD_FILE_NAME = "veritas-infoscale.tgz"
_DEAFULT_INSTALL_RESPONSE_FILE_NAME = "install.response"
_DEAFULT_UNINSTALL_RESPONSE_FILE_NAME = "uninstall.response"


def process(installer_download_info, downloader, packer):
    installer_tar_file = downloader.download(
        installer_download_info.installer_tar_url,
        veritas.LEAPP_VERITAS_DIR,
        _DEAFULT_DOWNLOAD_FILE_NAME
    )
    install_response_file = downloader.download(
        installer_download_info.install_response_file_url,
        veritas.LEAPP_VERITAS_DIR,
        _DEAFULT_INSTALL_RESPONSE_FILE_NAME
    )
    uninstall_response_file = downloader.download(
        installer_download_info.uninstall_response_file_url,
        veritas.LEAPP_VERITAS_DIR,
        _DEAFULT_UNINSTALL_RESPONSE_FILE_NAME
    )

    installers = _unpack_installer_tar_file(packer, installer_tar_file)
    uninstaller_path = installers.get('rhel7')
    installer_path = installers.get('rhel8')

    if not uninstaller_path:
        raise StopActorExecution('Failed to extract the rhel7 installer')
    if not installer_path:
        raise StopActorExecution('Failed to extract the rhel8 installer')

    return VeritasInstallerInfo(
        uninstaller_path=uninstaller_path,
        uninstall_response_path=uninstall_response_file,
        installer_path=installer_path,
        install_response_path=install_response_file,
    )


def _unpack_installer_tar_file(packer, tarfile_path):
    packer.unpack(tarfile_path, veritas.LEAPP_VERITAS_DIR)
    return _find_installers(veritas.LEAPP_VERITAS_DIR)


def _find_installers(path):
    installers = {}
    for root, _dirs, files in os.walk(path):
        installer_files = [f for f in files if f == 'installer']
        if not installer_files:
            continue
        path = os.path.join(path, root, installer_files[0])
        if os.path.dirname(path).startswith('rhel7'):
            installers['rhel7'] = path
        elif os.path.dirname(path).startswith('rhel8'):
            installers['rhel8'] = path
    return installers
