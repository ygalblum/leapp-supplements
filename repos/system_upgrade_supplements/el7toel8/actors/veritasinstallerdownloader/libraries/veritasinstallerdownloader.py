import errno
import os

from leapp.exceptions import StopActorExecution
from leapp.libraries.common import veritas
from leapp.models import VeritasInstallerInfo, VeritasInstallerPatchInfo

_DEAFULT_DOWNLOAD_FILE_NAME = "veritas-infoscale.tgz"
_DEAFULT_INSTALL_RESPONSE_FILE_NAME = "install.response"
_DEAFULT_UNINSTALL_RESPONSE_FILE_NAME = "uninstall.response"
_DEFAULT_PATCH_FILE_NAME_FORMAT = "patch-{index}.tgz"
_DEFAULT_PATCH_RESPONSE_FILE_NAME_FORMAT = "patch-{index}.response"


def process(installer_download_info, downloader, packer):
    installer_path, uninstaller_path = _download_and_unpack_ga_installer(installer_download_info, downloader, packer)
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

    patches = []
    for i, patch in enumerate(installer_download_info.patches):
        patches.append(_download_patch_and_response(i, patch, downloader, packer))

    return VeritasInstallerInfo(
        uninstaller_path=uninstaller_path,
        uninstall_response_path=uninstall_response_file,
        installer_path=installer_path,
        install_response_path=install_response_file,
        patches=patches
    )


def _download_and_unpack_ga_installer(installer_download_info, downloader, packer):
    installer_tar_file = downloader.download(
        installer_download_info.installer_tar_url,
        veritas.LEAPP_VERITAS_DIR,
        _DEAFULT_DOWNLOAD_FILE_NAME
    )

    packer.unpack(installer_tar_file, veritas.LEAPP_VERITAS_DIR)

    installers = _find_installers(veritas.LEAPP_VERITAS_DIR)
    uninstaller_path = installers.get('rhel7')
    installer_path = installers.get('rhel8')

    if not uninstaller_path:
        raise StopActorExecution('Failed to extract the rhel7 installer')
    if not installer_path:
        raise StopActorExecution('Failed to extract the rhel8 installer')

    return installer_path, uninstaller_path


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


def _download_patch_and_response(index, patch, downloader, packer):
    tar_file = downloader.download(
        patch.url,
        veritas.LEAPP_VERITAS_DIR,
        _DEFAULT_PATCH_FILE_NAME_FORMAT.format(index=index)
    )
    patch_path = _create_patch_dir(index)
    packer.unpack(tar_file, patch_path)
    patch_filename=_find_installer_bin(patch_path)
    response_file = downloader.download(
        patch.response_file,
        patch_path,
        _DEFAULT_PATCH_RESPONSE_FILE_NAME_FORMAT.format(index=index)
    )
    return VeritasInstallerPatchInfo(path=patch_filename, response_file_path=response_file)


def _create_patch_dir(index):
    patch_path = os.path.join(veritas.LEAPP_VERITAS_DIR, "patch-{index}".format(index=index))
    try:
        os.makedirs(patch_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(patch_path):
            pass
        else:
            raise
    return patch_path


def _find_installer_bin(root_path):
    patch_root_files = [os.path.join(root_path, f) for f in os.listdir(root_path)]
    patch_filename = [f for f in patch_root_files if os.path.isfile(f) and os.access(f, os.X_OK)]
    if len(patch_filename) > 1:
        patch_filename = [f for f in patch_filename if 'install' in f]
    if len(patch_filename) > 1:
        raise StopActorExecution(
            'Found {count} executables cannot determine which one is the executable'.format(count=len(patch_filename))
        )
    if not patch_filename:
        raise StopActorExecution('Could not find any executables')
    return patch_filename[0]
