import os
import mock

from leapp.libraries.actor import veritasinstaller
from leapp.models import VeritasInstallerInfo


output_directory = "/root/leapp-veritas"
rhel7_installer_path = os.path.join(output_directory, "rhel7", "installer")
rhel8_installer_path = os.path.join(output_directory, "rhel8", "installer")
uninstall_response_path = os.path.join(output_directory, "uninstall.response")
install_response_path = os.path.join(output_directory, "other_name_install.response")
vcs_backup_tgz = os.path.join(output_directory, "vcs-backup.tgz")


def test_veritas_uninstaller():
    installer_info = VeritasInstallerInfo(
            uninstaller_path=rhel7_installer_path,
            uninstall_response_path=uninstall_response_path,
            installer_path=rhel8_installer_path,
            install_response_path=install_response_path,
        )
    packer_mock = mock.MagicMock()
    command_runner_mock = mock.MagicMock()

    veritasinstaller.process(installer_info, packer_mock, command_runner_mock)
    packer_mock.unpack.assert_has_calls([mock.call(vcs_backup_tgz, '/')])
    command_runner_mock.call.assert_has_calls(
        [
            mock.call(
                [
                    '/root/leapp-veritas/rhel8/installer',
                    '-responsefile',
                    '/root/leapp-veritas/other_name_install.response'
                ]
            )
        ]
    )
