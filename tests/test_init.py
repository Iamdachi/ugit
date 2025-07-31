# test_init.py
import os
import pytest
from ugit.data import init  # Replace with your actual module

GIT_DIR = ".ugit"  # Replace if not a constant

@pytest.fixture
def git_dir():
    return GIT_DIR

def test_init_when_repo_exists(mocker, capsys, git_dir):
    mocker.patch("os.path.exists", return_value=True)
    makedirs = mocker.patch("os.makedirs")

    init()

    makedirs.assert_not_called()
    out = capsys.readouterr().out
    assert "Error: Repository already exists." in out

def test_init_creates_directories(mocker, git_dir):
    mocker.patch("os.path.exists", return_value=False)
    makedirs = mocker.patch("os.makedirs")

    init()

    expected_calls = [
        mocker.call(git_dir),
        mocker.call(os.path.join(git_dir, "objects"))
    ]
    makedirs.assert_has_calls(expected_calls, any_order=False)
