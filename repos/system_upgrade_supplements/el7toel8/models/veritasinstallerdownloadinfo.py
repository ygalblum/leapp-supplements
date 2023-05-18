from leapp.models import Model, fields
from leapp.topics import VeritasInstallerDownloadInfoTopic


class VeritasInstallerDownloadInfo(Model):
    topic = VeritasInstallerDownloadInfoTopic
    installer_tar_url = fields.String()
    install_response_file_url = fields.String()
    uninstall_response_file_url = fields.String()
