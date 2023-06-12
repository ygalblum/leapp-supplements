import json
import mock

from leapp.libraries.actor import veritasinstallerdownloadinfogatherer
from leapp.libraries.common import downloader
from leapp.models import VeritasInstallerDownloadInfo, VeritasInstallerPatchDownloadInfo


ga_installer_path = "http://example.com/ga_installer.tgz"
install_response_path = "http://example.com/install.response"
uninstall_response_path = "http://example.com/uninstall.response"
patches = [
    {
        "url": "http://example.com/patch_{index}/installer.tgz".format(index=i),
        "response_file": "http://example.com/patch_{index}/patch.response".format(index=i),
    } for i in range(3)
]
json_file_content = {
    "ga_installer": ga_installer_path,
    "install_response": install_response_path,
    "uninstall_response": uninstall_response_path,
    "patches": patches
}
expected_installer_download_info = VeritasInstallerDownloadInfo(
        installer_tar_url=ga_installer_path,
        install_response_file_url=install_response_path,
        uninstall_response_file_url=uninstall_response_path,
        patches=[VeritasInstallerPatchDownloadInfo(url=p['url'], response_file=p['response_file']) for p in patches],
    )


def test_veritasinstallerdownloadinfogatherer_url():
    json_file_url = "http://example.com/json_file.json"

    downloader_mock = mock.MagicMock(name='downloader', spec=downloader.Downloader)
    downloader_mock.get = mock.MagicMock(return_value=json_file_content)

    installer_download_info = veritasinstallerdownloadinfogatherer.process(json_file_url, downloader_mock)

    downloader_mock.get.assert_called_once_with(json_file_url)
    assert installer_download_info == expected_installer_download_info


def test_veritasinstallerdownloadinfogatherer_local(monkeypatch):
    json_file_path = "/etc/leapp/json_file.json"

    downloader_mock = mock.MagicMock(name='downloader', spec=downloader.Downloader)
    downloader_mock.get = mock.MagicMock()

    with mock.patch(
            "leapp.libraries.actor.veritasinstallerdownloadinfogatherer.open",
            mock.mock_open(read_data=json.dumps(json_file_content))
    ):
        installer_download_info = veritasinstallerdownloadinfogatherer.process(json_file_path, downloader_mock)

    downloader_mock.get.assert_not_called()
    assert installer_download_info == expected_installer_download_info
