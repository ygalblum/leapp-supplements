from functools import partial
import os

from leapp.libraries.common import veritas
from leapp.libraries.common.packer import PackerDirectory


def process(installer_info, packer, command_runner):
    command_runner.call(["/opt/VRTS/bin/hastop", "-local"])
    _save_configuration(packer)
    command_runner.call(
        [
            installer_info.uninstaller_path,
            "-responsefile",
            installer_info.uninstall_response_path
        ]
    )


def _save_configuration(packer):
    def _has_extension(ext, tar_info):
        return os.path.splitext(tar_info.name) == ext

    directories_to_backup = [
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
        PackerDirectory(path="/etc/VRTSvcs/conf/config", filter=partial(_has_extension, "cf"))
    ]

    packer.pack(veritas.CONFIG_BACKUP_TAR, directories_to_backup)
