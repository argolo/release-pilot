import os
from unittest.mock import patch

import pytest

import release_pilot


# ============================================================
# Utils & filesystem
# ============================================================

def test_list_directories_returns_sorted_directories(tmp_path):
    (tmp_path / "b").mkdir()
    (tmp_path / "a").mkdir()
    (tmp_path / "file.txt").write_text("x")

    result = release_pilot.list_directories(tmp_path)

    assert result == ["a", "b"]


def test_list_directories_invalid_path_returns_empty_list():
    assert release_pilot.list_directories("/path/that/does/not/exist") == []


def test_get_project_name_uses_current_directory(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert release_pilot.get_project_name() == tmp_path.name


# ============================================================
# Git helpers
# ============================================================

@patch("subprocess.run")
def test_get_git_branch_success(mock_run):
    mock_run.return_value.stdout = "main\n"

    branch = release_pilot.get_git_branch()

    assert branch == "main"


@patch("subprocess.run", side_effect=Exception)
def test_get_git_branch_fallback_to_unknown(_):
    assert release_pilot.get_git_branch() == "unknown"


# ============================================================
# Command planning (core responsibility)
# ============================================================

def generate_commands(contractors, environments_map, platforms, commands):
    """
    Local helper mirroring ReleasePilot planning logic.
    """
    planned = []

    for contractor in contractors:
        for environment in environments_map[contractor]:
            for platform in platforms:
                for command in commands:
                    planned.append(
                        f"yarn {platform}:{contractor}:{environment}:{command}"
                    )

    return planned


def test_command_generation_order_is_deterministic():
    contractors = ["quickup", "kompa"]
    environments_map = {
        "quickup": ["sandbox"],
        "kompa": ["beta"],
    }
    platforms = ["android", "ios"]
    commands = ["add", "build"]

    result = generate_commands(
        contractors,
        environments_map,
        platforms,
        commands,
    )

    assert result == [
        "yarn android:quickup:sandbox:add",
        "yarn android:quickup:sandbox:build",
        "yarn ios:quickup:sandbox:add",
        "yarn ios:quickup:sandbox:build",
        "yarn android:kompa:beta:add",
        "yarn android:kompa:beta:build",
        "yarn ios:kompa:beta:add",
        "yarn ios:kompa:beta:build",
    ]


# ============================================================
# Command execution (mocked)
# ============================================================

@patch("subprocess.run")
def test_run_command_executes_subprocess(mock_run):
    release_pilot.run_command("echo test")

    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args

    assert "echo test" in args
    assert kwargs["shell"] is True
    assert kwargs["check"] is True


# ============================================================
# Human checkpoints
# ============================================================

@patch("builtins.input", return_value="")
def test_wait_for_confirmation_does_not_raise(mock_input):
    release_pilot.wait_for_confirmation("testing pause")
    mock_input.assert_called_once()


# ============================================================
# Interactive selection
# ============================================================

@patch("builtins.input", side_effect=["1"])
def test_choose_option_single_selection(_):
    result = release_pilot.choose_option("Test", ["a", "b"])
    assert result == ["a"]


@patch("builtins.input", side_effect=["3"])
def test_choose_option_all_expands(_):
    result = release_pilot.choose_option("Test", ["a", "b"])
    assert result == ["a", "b"]


# ============================================================
# Constants sanity check
# ============================================================

def test_supported_platforms_are_not_empty():
    assert "android" in release_pilot.PLATFORMS
    assert "ios" in release_pilot.PLATFORMS


def test_command_order_is_respected():
    assert release_pilot.COMMANDS_ORDER == ["add", "build"]
