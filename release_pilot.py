#!/usr/bin/env python3
"""
ReleasePilot - Release Orchestrator

A CLI tool to orchestrate yarn commands for white-label application builds,
ensuring deterministic execution order, human-assisted checkpoints and
full release traceability.
"""

import os
import subprocess
import sys
from typing import List, Dict


# =========================
# ANSI COLORS (Purple theme)
# =========================
PURPLE = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


def purple(text: str) -> str:
    """
    Wrap text with purple ANSI color.

    >>> purple("test")  # doctest: +ELLIPSIS
    '\\x1b[95mtest\\x1b[0m'
    """
    return f"{PURPLE}{text}{RESET}"


# =========================
# CONSTANTS
# =========================
BASE_CONTRACTOR_PATH = "./contractor"
PLATFORMS = ["android", "ios"]
COMMANDS_ORDER = ["add", "build"]


def choose_option(title: str, options: List[str]) -> List[str]:
    """
    Display an interactive menu and return the selected option(s).

    Supports a special '(all)' option that expands to all available choices.

    :param title: Menu title
    :param options: Available options
    :return: A list of selected options
    """
    options_with_all = options + ["(all)"]

    print(purple(f"\n▶ {title}"))
    for idx, option in enumerate(options_with_all, start=1):
        print(purple(f"{idx}. {option}"))

    while True:
        try:
            choice = int(input(purple("Select an option: ")))
            if 1 <= choice <= len(options_with_all):
                selected = options_with_all[choice - 1]
                return options if selected == "(all)" else [selected]
        except ValueError:
            pass
        print(purple("⚠ Invalid option. Please try again."))


def list_directories(path: str) -> List[str]:
    """
    List subdirectories for a given path.

    :param path: Base directory
    :return: Sorted list of directory names
    """
    if not os.path.isdir(path):
        return []

    return sorted(
        name
        for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
    )


def run_command(command: str) -> None:
    """
    Execute a shell command using subprocess.

    :param command: Command to execute
    :raises subprocess.CalledProcessError: If command fails
    """
    print(purple(f"\n🚀 Running: {command}"))
    subprocess.run(command, shell=True, check=True)


def wait_for_confirmation(reason: str) -> None:
    """
    Pause execution until the user confirms continuation.

    :param reason: Context explaining why execution is paused
    """
    print(purple(f"\n⏸ Execution paused: {reason}"))
    input(purple("Press ENTER to continue..."))


def get_git_branch() -> str:
    """
    Retrieve the current Git branch.

    :return: Branch name or 'unknown' if unavailable
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def get_project_name() -> str:
    """
    Infer project name from the current working directory.

    >>> isinstance(get_project_name(), str)
    True
    """
    return os.path.basename(os.getcwd())


def print_release_summary(
    *,
    contractors: List[str],
    environments_map: Dict[str, List[str]],
    platforms: List[str],
    total_commands: int,
) -> None:
    """
    Print a technical and human-readable release summary.

    :param contractors: List of contractors involved
    :param environments_map: Mapping of contractors to environments
    :param platforms: Platforms involved in the release
    :param total_commands: Total executed commands
    """
    project_name = get_project_name()
    git_branch = get_git_branch()

    contractors_str = ", ".join(contractors)
    all_envs = sorted({env for envs in environments_map.values() for env in envs})
    environments_str = ", ".join(all_envs)
    platforms_str = ", ".join(platforms)

    print("\n" + purple("=" * 70))
    print(purple(f"{BOLD}🚀 RELEASE SUMMARY{RESET}"))
    print(purple("=" * 70))
    print(purple(f"📁 Project      : {project_name}"))
    print(purple(f"🌿 Git Branch   : {git_branch}"))
    print(purple(f"📦 Contractors : {contractors_str}"))
    print(purple(f"🧪 Environments: {environments_str}"))
    print(purple(f"📱 Platforms   : {platforms_str}"))
    print(purple("=" * 70))


def main() -> None:
    """
    Main entry point for ReleasePilot.
    """
    executed_commands: List[str] = []

    print(purple(f"\n{BOLD}=== 🧰 ReleasePilot | Release Orchestrator ==={RESET}"))

    platforms = choose_option("Platform", PLATFORMS)
    contractors = choose_option(
        "Contractor",
        list_directories(BASE_CONTRACTOR_PATH),
    )

    environments_map: Dict[str, List[str]] = {}
    for contractor in contractors:
        env_path = os.path.join(BASE_CONTRACTOR_PATH, contractor)
        environments_map[contractor] = choose_option(
            f"Environment ({contractor})",
            list_directories(env_path),
        )

    commands = choose_option("Command", COMMANDS_ORDER)
    commands = [cmd for cmd in COMMANDS_ORDER if cmd in commands]

    planned_commands: List[str] = []

    print(purple("\n📌 Execution plan:"))
    for contractor in contractors:
        for environment in environments_map[contractor]:
            for platform in platforms:
                for command in commands:
                    yarn_cmd = f"yarn {platform}:{contractor}:{environment}:{command}"
                    planned_commands.append(yarn_cmd)
                    print(purple(yarn_cmd))

    confirm = input(purple("\nConfirm execution? (y/N): ")).strip().lower()
    if confirm != "y":
        print(purple("⏹ Execution cancelled."))
        sys.exit(0)

    try:
        for contractor in contractors:
            for environment in environments_map[contractor]:
                for platform in platforms:
                    for command in commands:
                        yarn_cmd = f"yarn {platform}:{contractor}:{environment}:{command}"
                        run_command(yarn_cmd)
                        executed_commands.append(yarn_cmd)

                if environment != environments_map[contractor][-1]:
                    wait_for_confirmation(
                        f"Environment '{environment}' completed for '{contractor}'"
                    )

            if contractor != contractors[-1]:
                wait_for_confirmation(f"Contractor '{contractor}' completed")

    except subprocess.CalledProcessError as exc:
        print(purple(f"\n❌ Command failed (exit code {exc.returncode})"))
        sys.exit(exc.returncode)

    print_release_summary(
        contractors=contractors,
        environments_map=environments_map,
        platforms=platforms,
        total_commands=len(executed_commands),
    )

    print(purple("\n📋 Executed commands:\n"))
    for idx, cmd in enumerate(executed_commands, start=1):
        print(purple(f"{idx:02d}. {cmd}"))


if __name__ == "__main__":
    main()
