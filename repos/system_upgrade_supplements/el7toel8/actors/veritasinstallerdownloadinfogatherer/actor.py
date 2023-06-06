from leapp import reporting
from leapp.actors import Actor
from leapp.dialogs import Dialog
from leapp.dialogs.components import TextComponent
from leapp.libraries.common.rpms import has_package
from leapp.models import VeritasInstallerDownloadInfo, InstalledRPM
from leapp.tags import IPUWorkflowTag, ChecksPhaseTag


class VeritasInstallerDownloadInfoGatherer(Actor):
    """
    No documentation has been provided for the veritas_installer_download_info_gatherer actor.
    """

    name = 'veritas_installer_download_info_gatherer'
    consumes = (InstalledRPM,)
    produces = (VeritasInstallerDownloadInfo, reporting.Report)
    tags = (IPUWorkflowTag, ChecksPhaseTag)
    dialogs = (
        Dialog(
            scope='veritas_installer_download_info_gatherer',
            reason='Veritas Infoscale has a standalone installer. '
            'The upgrade process will download it from the provided URL, '
            'uninstall Infoscale before the upgrade using the RHEL7 installer and the uninstall response file, '
            'and install it afterwards using the RHEL8 installer and the install response file',
            components=(
                TextComponent(
                    key='installer',
                    label='Please provide the URL to download the installation TGZ package from',
                    description='The installation package will to uninstall and install Veritas Infoscale'
                ),
                TextComponent(
                    key='uninstaller_response',
                    label='Please provide the URL to download the responses file '
                    'to use when uninstalling Veritas Infoscale',
                    description='The upgrade process will uninstall Infoscale using the uninstall response file',
                ),
                TextComponent(
                    key='installer_response',
                    label='Please provide the URL to download the responses file '
                    'to use when installing Veritas Infoscale',
                    description='The upgrade process will install Infoscale using the install response file',
                ),
            ),
        ),
    )

    def process(self):
        self.log.info("Checking if Veritas infoscale is installed")
        if has_package(InstalledRPM, 'VRTSpython'):
            answers = self.get_answers(self.dialogs[0])
            if answers:
                self.produce(
                    VeritasInstallerDownloadInfo(
                        installer_tar_url=answers.get('installer'),
                        install_response_file_url=answers.get('installer_response'),
                        uninstall_response_file_url=answers.get('uninstaller_response'),
                    )
                )
                reporting.create_report([
                    reporting.Title('An installation of Veritas Infoscale was found'),
                    reporting.Summary(
                        'Veritas Infoscale does not support upgrading from RHEL7 to RHEL8. '
                        'Instead, the configuration of the current deployment will be stored, '
                        'and Infoscale will be removed before the upgrade. '
                        'Once the upgrade is complete, Infoscale will be re-installed '
                        'and the configuration will be restored'
                    ),
                    reporting.Severity(reporting.Severity.INFO),
                    reporting.Groups([reporting.Groups.HIGH_AVAILABILITY]),
                ])
