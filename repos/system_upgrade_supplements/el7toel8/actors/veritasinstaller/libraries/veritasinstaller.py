from leapp.libraries.common import veritas


def process(installer_info, packer, command_runner):
    packer.unpack(veritas.CONFIG_BACKUP_TAR, "/")
    command_runner.call(
        [
            installer_info.installer_path,
            "-responsefile",
            installer_info.install_response_path
        ]
    )
