import mock
from leapp.libraries.actor import simple


def test_from_actor(current_actor_context):
    with mock.patch("leapp.libraries.actor.simple._subprocess_call") as m:
        current_actor_context.run()
        m.assert_has_calls(
            calls=[
                mock.call(["/opt/non_existing/bin/run", "from_actor"]),
            ]
        )


def test_from_test():
    with mock.patch("leapp.libraries.actor.simple._subprocess_call") as m:
        simple.run_non_existing_bin("from_test")
        m.assert_has_calls(
            calls=[
                mock.call(["/opt/non_existing/bin/run", "from_test"])
            ]
        )
