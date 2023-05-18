from leapp.actors import Actor
from leapp.libraries.actor import veritasuninstaller
from leapp.libraries.common import packer, command_runner
from leapp.models import VeritasInstallerInfo
from leapp.tags import IPUWorkflowTag, InterimPreparationPhaseTag


class VeritasUninstaller(Actor):
    """
    No documentation has been provided for the veritas_uninstaller actor.
    """

    name = 'veritas_uninstaller'
    consumes = (VeritasInstallerInfo,)
    produces = ()
    tags = (IPUWorkflowTag, InterimPreparationPhaseTag)

    def process(self):
        installer_info = next(self.consume(VeritasInstallerInfo))

        veritasuninstaller.process(installer_info, packer.Packer(), command_runner.CommandRunner())
