from leapp.models import Model, fields
from leapp.topics import VeritasInstallerInfoTopic


class VeritasInstallerInfo(Model):
    topic = VeritasInstallerInfoTopic
    uninstaller_path = fields.String()
    uninstall_response_path = fields.String()
    installer_path = fields.String()
    install_response_path = fields.String()
