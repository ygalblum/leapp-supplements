import requests

from leapp import reporting
from leapp.actors import Actor
from leapp.dialogs import Dialog
from leapp.dialogs.components import TextComponent
from leapp.libraries.actor import veritasinstallerdownloadinfogatherer
from leapp.libraries.common import downloader
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
            reason='Veritas Infoscale is installed using a standalone installer and patches. '
            'The upgrade process requires a list of the URLs of the GA installer, '
            'patches and response files for each step. '
            'The upgrade process will download all the files from the provided URLs during the Download phase '
            'The upgrade process will uninstall Infoscale before the upgrade '
            'using the GA RHEL7 installer and the uninstall response file, '
            'The upgrade process will install Infoscale after the upgrade '
            'using the RHEL8 GA installer and the install response file'
            'The upgrade process will install all the provided patches using their corresponding response files '
            'The list should be provided in a json file with the following keys: '
            'ga_installer, uninstall_response, install_response and '
            'an array named patches of objects with the keys url and response_file '
            'ga_installer and patch are URLs for the corresponding TGZ files '
            'uninstall_response, install_response and response_file are URLs for the corresponding response files. '
            'The JSON file maybe passed as a local path or a URL',
            components=(
                TextComponent(
                    key='json_file',
                    label='Please provide the URL of the JSON file',
                    description='The JSON file will include the information for downloading all the required files.'
                ),
            ),
        ),
    )

    def process(self):
        self.log.info("Checking if Veritas infoscale is installed")
        if has_package(InstalledRPM, 'VRTSpython'):
            answers = self.get_answers(self.dialogs[0])
            if answers:
                groups = [reporting.Groups.HIGH_AVAILABILITY]

                json_file = answers.get('json_file')
                try:
                    installer_download_info = veritasinstallerdownloadinfogatherer.process(
                        json_file,
                        downloader.Downloader(),
                    )
                except (OSError, requests.exceptions.HTTPError):
                    severity = reporting.Severity.HIGH
                    groups.append(reporting.Groups.INHIBITOR)
                    success_or_failure_info = 'Failed to process the URL Info JSON file: {json_file}'.format(
                        json_file=json_file
                    )
                else:
                    severity = reporting.Severity.INFO
                    success_or_failure_info = 'The URL Info JSON file was processed successfully'
                    self.produce(installer_download_info)

                reporting.create_report([
                    reporting.Title('An installation of Veritas Infoscale was found'),
                    reporting.Summary(
                        'Veritas Infoscale does not support upgrading from RHEL7 to RHEL8. '
                        'Instead, the configuration of the current deployment will be stored, '
                        'and Infoscale will be removed before the upgrade. '
                        'Once the upgrade is complete, Infoscale will be re-installed '
                        'and the configuration will be restored. ' + success_or_failure_info
                    ),
                    reporting.Severity(severity),
                    reporting.Groups([reporting.Groups.HIGH_AVAILABILITY]),
                ])
