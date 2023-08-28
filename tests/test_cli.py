import pytest
from click.testing import CliRunner
from readercli.commands import list, add, upload


@pytest.fixture
def runner():
    return CliRunner()


def test_list_with_options(runner):
    result = runner.invoke(list, ["--location", "archive", "--layout", "list"])
    assert result.exit_code == 0


def test_add_document(runner):
    result = runner.invoke(add, ["https://example.com"])
    assert result.exit_code == 0


def test_upload_reading_list(runner):
    with runner.isolated_filesystem():
        with open("test_reading_list.html", "w") as f:
            f.write("<html><body>Document URLs</body></html>")
        result = runner.invoke(
            upload, ["test_reading_list.html", "--file-type", "html"]
        )
        assert result.exit_code == 0


def test_list_help(runner):
    result = runner.invoke(list, ["--help"])
    assert result.exit_code == 0


def test_add_help(runner):
    result = runner.invoke(add, ["--help"])
    assert result.exit_code == 0


def test_upload_help(runner):
    result = runner.invoke(upload, ["--help"])
    assert result.exit_code == 0
