from leapp.libraries.actor import veritasinstallerdownloadinfogatherer
from leapp.models import InstalledRPM, RPM, VeritasInstallerDownloadInfo, VeritasInstallerPatchDownloadInfo
from leapp.reporting import Report


def test_actor_with_veritas_python_package(monkeypatch, current_actor_context):
    with_veritas = [
            RPM(name='VRTSpython',
                epoch='2',
                packager='Veritas',
                version='8.0.0',
                release='0.0.el7_9',
                arch='x86_64',
                pgpsig='RSA/SHA256, Fri 07 Jan 2022 01:50:17 PM UTC, Key ID 199e2f91fd431d51',
                repository='installed',
                module=None,
                stream=None),
            RPM(name='grep',
                epoch='0',
                packager='Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>',
                version='2.20',
                release='3.el7',
                arch='x86_64',
                pgpsig='RSA/SHA256, Fri 24 Mar 2017 04:59:11 PM UTC, Key ID 199e2f91fd431d51',
                repository='anaconda/7.9',
                module=None,
                stream=None)
            ]

    def mocked_input(_title):
        return "http://example.com/info.json"

    monkeypatch.setattr('leapp.dialogs.renderer.input', mocked_input)

    ga_installer_path = "http://example.com/ga_installer.tgz"
    install_response_path = "http://example.com/install.response"
    uninstall_response_path = "http://example.com/uninstall.response"
    patches = [
        {
            "url": "http://example.com/patch_{index}/installer.tgz".format(index=i),
            "response_file": "http://example.com/patch_{index}/patch.response".format(index=i),
        } for i in range(3)
    ]
    expected_installer_download_info = VeritasInstallerDownloadInfo(
        installer_tar_url=ga_installer_path,
        install_response_file_url=install_response_path,
        uninstall_response_file_url=uninstall_response_path,
        patches=[VeritasInstallerPatchDownloadInfo(url=p['url'], response_file=p['response_file']) for p in patches],
    )
    monkeypatch.setattr(
        veritasinstallerdownloadinfogatherer,
        "process",
        lambda _x, _y: expected_installer_download_info
    )

    current_actor_context.feed(InstalledRPM(items=with_veritas))

    current_actor_context.run()

    assert current_actor_context.consume(Report)
    installer_download_info = current_actor_context.consume(VeritasInstallerDownloadInfo)
    assert installer_download_info
    installer_download_info = installer_download_info[0]
    assert installer_download_info == expected_installer_download_info


def test_actor_without_veritas_python_package(current_actor_context):
    without_docker = [
            RPM(name='tree',
                epoch='0',
                packager='Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>',
                version='1.6.0',
                release='10.el7',
                arch='x86_64',
                pgpsig='RSA/SHA256, Wed 02 Apr 2014 09:33:48 PM UTC, Key ID 199e2f91fd431d51',
                repository='installed',
                module=None,
                stream=None),
            RPM(name='grep',
                epoch='0',
                packager='Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>',
                version='2.20',
                release='3.el7',
                arch='x86_64',
                pgpsig='RSA/SHA256, Fri 24 Mar 2017 04:59:11 PM UTC, Key ID 199e2f91fd431d51',
                repository='anaconda/7.9',
                module=None,
                stream=None)
            ]

    current_actor_context.feed(InstalledRPM(items=without_docker))
    current_actor_context.run()
    assert not current_actor_context.consume(Report)
    assert not current_actor_context.consume(VeritasInstallerDownloadInfo)
