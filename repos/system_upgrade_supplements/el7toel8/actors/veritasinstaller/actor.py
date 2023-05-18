from leapp.actors import Actor
from leapp.libraries.actor import veritasinstaller
from leapp.libraries.common import packer, command_runner
from leapp.models import VeritasInstallerInfo
from leapp.tags import IPUWorkflowTag, FirstBootPhaseTag


class VeritasInstaller(Actor):
    """
    No documentation has been provided for the veritas_installer actor.
    """

    name = 'veritas_installer'
    consumes = (VeritasInstallerInfo,)
    produces = ()
    tags = (IPUWorkflowTag, FirstBootPhaseTag)

    def process(self):
        installer_info = next(self.consume(VeritasInstallerInfo))

        veritasinstaller.process(installer_info, packer.Packer(), command_runner.CommandRunner())
