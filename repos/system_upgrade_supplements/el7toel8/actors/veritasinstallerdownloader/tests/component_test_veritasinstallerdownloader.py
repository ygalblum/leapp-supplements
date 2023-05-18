import os

from leapp.libraries.actor import veritasinstallerdownloader
from leapp.models import VeritasInstallerDownloadInfo, VeritasInstallerInfo

installer_location = "http://www.example.com/download/installer"
uninstall_response_location = "http://www.example.com/download/uninstall.response"
install_response_location = "http://www.example.com/download/install.response"

default_download_file_name = "veritas-infoscale.tgz"
default_install_response_file_name = "install.response"
default_uninstall_response_file_name = "uninstall.response"

output_directory = "/root/leapp-veritas"
rhel7_installer_path = os.path.join(output_directory, "rhel7", "installer")
rhel8_installer_path = os.path.join(output_directory, "rhel8", "installer")
install_response_file_path = os.path.join(output_directory, default_install_response_file_name)
uninstall_response_file_path = os.path.join(output_directory, default_uninstall_response_file_name)


def test_veritas_installer_downloader(monkeypatch, current_actor_context):
    expected_installer_info = VeritasInstallerInfo(
        uninstaller_path=rhel7_installer_path,
        uninstall_response_path=uninstall_response_file_path,
        installer_path=rhel8_installer_path,
        install_response_path=install_response_file_path
    )
    monkeypatch.setattr(
        veritasinstallerdownloader,
        "process",
        lambda x, y, z: expected_installer_info
    )

    current_actor_context.feed(
        VeritasInstallerDownloadInfo(
            installer_tar_url=installer_location,
            install_response_file_url=install_response_location,
            uninstall_response_file_url=uninstall_response_location
        )
    )
    current_actor_context.run()
    actual_installer_info = current_actor_context.consume(VeritasInstallerInfo)
    assert actual_installer_info
    actual_installer_info = actual_installer_info[0]
    assert actual_installer_info == expected_installer_info
