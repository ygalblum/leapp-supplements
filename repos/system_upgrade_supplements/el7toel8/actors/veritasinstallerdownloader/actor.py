from leapp.actors import Actor
from leapp.libraries.actor import veritasinstallerdownloader
from leapp.libraries.common import downloader, packer
from leapp.models import VeritasInstallerDownloadInfo, VeritasInstallerInfo
from leapp.tags import IPUWorkflowTag, DownloadPhaseTag


class VeritasInstallerDownloader(Actor):
    """
    No documentation has been provided for the veritas_installer_downloader actor.
    """

    name = 'veritas_installer_downloader'
    consumes = (VeritasInstallerDownloadInfo,)
    produces = (VeritasInstallerInfo,)
    tags = (IPUWorkflowTag, DownloadPhaseTag)

    def process(self):
        installer_download_info = next(self.consume(VeritasInstallerDownloadInfo))

        installer_info = veritasinstallerdownloader.process(
            installer_download_info,
            downloader.Downloader(),
            packer.Packer()
        )

        self.produce(installer_info)
