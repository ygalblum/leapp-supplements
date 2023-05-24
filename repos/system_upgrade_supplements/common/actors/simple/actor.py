from leapp.actors import Actor
from leapp.libraries.actor import simple
from leapp.reporting import Report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class Simple(Actor):
    """
    The Simple actor is used to check the mock system
    """

    name = "simple"
    consumes = ()
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        simple.run_non_existing_bin("from_actor")
