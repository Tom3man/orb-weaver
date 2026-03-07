from unittest.mock import patch

from orb import __version__
from orb.cli import main


@patch("sys.argv", ["orb", "version"])
def test_cli_version(capsys):
    assert main() == 0
    output = capsys.readouterr().out.strip()
    assert output == __version__


@patch("sys.argv", ["orb", "user-agent"])
@patch("orb.cli.GetUserAgent")
def test_cli_user_agent(mock_ua, capsys):
    mock_ua.return_value.headers_dict = {"User-Agent": "UA"}
    assert main() == 0
    output = capsys.readouterr().out
    assert "User-Agent" in output
