from leapp.models import Model, fields
from leapp.topics import VeritasInstallerDownloadInfoTopic


class VeritasInstallerPatchDownloadInfo(Model):
    topic = VeritasInstallerDownloadInfoTopic
    url = fields.String()
    response_file = fields.String()


class VeritasInstallerDownloadInfo(Model):
    topic = VeritasInstallerDownloadInfoTopic
    installer_tar_url = fields.String()
    install_response_file_url = fields.String()
    uninstall_response_file_url = fields.String()
    patches = fields.List(fields.Model(VeritasInstallerPatchDownloadInfo), default=[])
