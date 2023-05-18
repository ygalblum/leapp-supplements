import os
from leapp.libraries.actor import veritasuninstaller
from leapp.libraries.common.packer import PackerDirectory, Packer
from leapp.libraries.common.command_runner import CommandRunner
from leapp.models import VeritasInstallerInfo
import mock


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
    packer_mock = mock.MagicMock(spec=Packer)
    command_runner_mock = mock.MagicMock(spec=CommandRunner)

    veritasuninstaller.process(installer_info, packer_mock, command_runner_mock)

    veritas_configuration_directories = [
        PackerDirectory(path="/etc/llthosts", filter=None),
        PackerDirectory(path="/etc/llttab", filter=None),
        PackerDirectory(path="/etc/gabtab", filter=None),
        PackerDirectory(path="/etc/vx/volboot", filter=None),
        PackerDirectory(path="/etc/sysconfig/vcs", filter=None),
        PackerDirectory(path="/etc/sysconfig/gab", filter=None),
        PackerDirectory(path="/etc/sysconfig/llt", filter=None),
        PackerDirectory(path="/etc/sysconfig/amf", filter=None),
        PackerDirectory(path="/etc/sysconfig/vxfen", filter=None),
        PackerDirectory(path="/etc/sysconfig/vcsmm", filter=None),
        PackerDirectory(path="/etc/vx/.uuids", filter=None),
        PackerDirectory(path="/etc/vxfenmode", filter=None),
        PackerDirectory(path="/etc/vxfentab", filter=None),
        PackerDirectory(path="/etc/VRTSvcs/conf/config", filter=mock.ANY)
    ]

    packer_mock.pack.assert_has_calls(
        [
            mock.call(vcs_backup_tgz, veritas_configuration_directories)
        ]
    )
    command_runner_mock.call.assert_has_calls(
        [
            mock.call(['/opt/VRTS/bin/hastop', '-local']),
            mock.call([rhel7_installer_path, '-responsefile', uninstall_response_path]),
        ]
    )
