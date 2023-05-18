from leapp.models import InstalledRPM, RPM, VeritasInstallerDownloadInfo
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

    installer_location = "http://www.example.com/download/installer"
    uninstall_response_location = "http://www.example.com/download/uninstall.response"
    install_response_location = "http://www.example.com/download/install.response"

    def mocked_input(title):
        if 'TGZ' in title:
            return installer_location
        if 'when uninstalling' in title:
            return uninstall_response_location
        if 'when installing' in title:
            return install_response_location
        return ""

    monkeypatch.setattr('leapp.dialogs.renderer.input', mocked_input)

    current_actor_context.feed(InstalledRPM(items=with_veritas))
    current_actor_context.run()
    assert current_actor_context.consume(Report)
    download_info = current_actor_context.consume(VeritasInstallerDownloadInfo)
    assert download_info
    download_info = download_info[0]

    assert download_info.installer_tar_url == installer_location
    assert download_info.install_response_file_url == install_response_location
    assert download_info.uninstall_response_file_url == uninstall_response_location


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
