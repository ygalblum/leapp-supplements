import os
import mock

from leapp.libraries.actor import veritasinstallerdownloader
from leapp.libraries.common import downloader
from leapp.models import VeritasInstallerDownloadInfo, VeritasInstallerPatchDownloadInfo, VeritasInstallerInfo


installer_location = "http://www.example.com/download/installer"
uninstall_response_location = "http://www.example.com/download/uninstall.response"
install_response_location = "http://www.example.com/download/install.response"

default_download_file_name = "veritas-infoscale.tgz"
default_install_response_file_name = "install.response"
default_uninstall_response_file_name = "uninstall.response"

output_directory = "/root/leapp-veritas"
rhel7_installer_path = os.path.join(output_directory, "rhel7", "installer")
rhel8_installer_path = os.path.join(output_directory, "rhel8", "installer")
installer_tgz_path = os.path.join(output_directory, default_download_file_name)
install_response_file_path = os.path.join(output_directory, default_install_response_file_name)
uninstall_response_file_path = os.path.join(output_directory, default_uninstall_response_file_name)


def test_veritas_installer_downloader_library(monkeypatch):
    installer_download_info = VeritasInstallerDownloadInfo(
        installer_tar_url=installer_location,
        install_response_file_url=install_response_location,
        uninstall_response_file_url=uninstall_response_location
        patches=[VeritasInstallerPatchDownloadInfo(url="", response_file="")]
    )
    downloader_mock = mock.MagicMock(name='downloader', spec=downloader.Downloader)
    downloader_mock.download = mock.MagicMock(
        side_effect=[
            installer_tgz_path,
            install_response_file_path,
            uninstall_response_file_path
        ]
    )
    packer_mock = mock.MagicMock()
    monkeypatch.setattr(
        veritasinstallerdownloader,
        '_find_installers',
        lambda _x: {'rhel7': rhel7_installer_path, 'rhel8': rhel8_installer_path}
    )

    actual_installer_info = veritasinstallerdownloader.process(installer_download_info, downloader_mock, packer_mock)
    downloader_mock.download.assert_has_calls(
        [
            mock.call(installer_location, output_directory, default_download_file_name),
            mock.call(install_response_location, output_directory, default_install_response_file_name),
            mock.call(uninstall_response_location, output_directory, default_uninstall_response_file_name),
        ],
    )
    packer_mock.unpack.assert_has_calls(
        [
            mock.call(installer_tgz_path, output_directory)
        ]
    )
    assert actual_installer_info == VeritasInstallerInfo(
        uninstaller_path=rhel7_installer_path,
        uninstall_response_path=uninstall_response_file_path,
        installer_path=rhel8_installer_path,
        install_response_path=install_response_file_path
    )
