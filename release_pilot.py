#!/usr/bin/env python3
import os
import subprocess
import sys

BASE_CONTRACTOR_PATH = "./contractor"

PLATFORMS = ["android", "ios"]
COMMANDS_ORDER = ["add", "build"]


def choose_option(title: str, options: list[str]) -> list[str]:
    options_with_all = options + ["(todas)"]

    print(f"\n🔹 {title}")
    for idx, option in enumerate(options_with_all, start=1):
        print(f"{idx}. {option}")

    while True:
        try:
            choice = int(input("Selecione uma opção: "))
            if 1 <= choice <= len(options_with_all):
                selected = options_with_all[choice - 1]
                return options if selected == "(todas)" else [selected]
        except ValueError:
            pass
        print("⚠️ Opção inválida. Tente novamente.")

def list_directories(path: str) -> list[str]:
    if not os.path.isdir(path):
        return []
    return sorted(
        name for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
    )

def run_command(command: str):
    print(f"\n🚀 Executando: {command}")
    subprocess.run(command, shell=True, check=True)

def wait_for_confirmation(reason: str):
    print(f"\n⏸️ Execução pausada: {reason}")
    input("👉 Pressione ENTER para continuar...")

def get_git_branch() -> str:
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
        return "desconhecida"
    
def get_project_name() -> str:
    return os.path.basename(os.getcwd())

def print_release_summary(
    *,
    contractors: list[str],
    environments_map: dict[str, list[str]],
    platforms: list[str],
    total_commands: int,
) -> None:
    project_name = get_project_name()
    contractors_str = ", ".join(contractors)

    all_envs = sorted(
        {env for envs in environments_map.values() for env in envs}
    )
    environments_str = ", ".join(all_envs)

    platforms_str = ", ".join(platforms)
    git_branch = get_git_branch()

    # --- Resumo técnico ---
    print("\n" + "=" * 60)
    print("🚀 RESUMO DA RELEASE")
    print("=" * 60)
    print(f"📁 Projeto      : {project_name}")
    print(f"🏷️ Versão       : {git_branch}")
    print(f"📦 Contratantes : {contractors_str}")
    print(f"🧪 Ambientes    : {environments_str}")
    print(f"📱 Plataformas  : {platforms_str}")
    print(f"⚙️ Comandos     : {total_commands}")
    print("=" * 60)

    # --- Mensagem humanizada ---
    contractor_main = contractors[0] if len(contractors) == 1 else contractors_str
    env_main = all_envs[0] if len(all_envs) == 1 else environments_str
    platforms_human = " e ".join(platforms)

    print(
        f"""
Pessoal,

Publicamos hoje a versão **{git_branch}** do **{project_name.upper()}** para **{contractor_main.upper()}** em **{env_main}**, para **{platforms_human.upper()}**. Essa release consolida as entregas da sprint em **{env_main}**, incluindo os ajustes e melhorias que trabalhamos.

⚠️ _Próximo passo: Para o iOS, é necessário responder o formulário de conformidade e solicitar a liberação na App Store Connect para concluir a publicação._

Se identificarem qualquer comportamento fora do esperado, peço que me sinalizem o mais breve possível para acompanharmos e contigências.
"""
    )
    print("") 


def main() -> None:
    executed_commands: list[str] = []

    print("\n=== 🧰 ReleasePilot: Release Orchestrator ===")

    platforms = choose_option("Plataforma", PLATFORMS)

    contractors = choose_option(
        "Contratante",
        list_directories(BASE_CONTRACTOR_PATH)
    )

    environments_map: dict[str, list[str]] = {}
    for contractor in contractors:
        env_path = os.path.join(BASE_CONTRACTOR_PATH, contractor)
        environments_map[contractor] = choose_option(
            f"Ambiente ({contractor})",
            list_directories(env_path)
        )

    commands = choose_option("Comando", COMMANDS_ORDER)
    commands = [cmd for cmd in COMMANDS_ORDER if cmd in commands]

    # Planejamento == Execução (fonte única de verdade)
    planned_commands: list[str] = []

    print("\n📌 Planejamento de execução:")
    for contractor in contractors:
        for environment in environments_map[contractor]:
            for platform in platforms:
                for command in commands:
                    yarn_cmd = f"yarn {platform}:{contractor}:{environment}:{command}"
                    planned_commands.append(yarn_cmd)
                    print(yarn_cmd)

    confirm = input("\nConfirmar execução? (y/N): ").strip().lower()
    if confirm != "y":
        print("⏹️ Execução cancelada.")
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
                        f"Ambiente '{environment}' finalizado para '{contractor}'"
                    )

            if contractor != contractors[-1]:
                wait_for_confirmation(
                    f"Contratante '{contractor}' finalizado"
                )

    except subprocess.CalledProcessError as exc:
        print(f"\n❌ Erro ao executar comando ({exc.returncode})")
        sys.exit(exc.returncode)

    print("\n=== ✅ Resumo Final ===")
    print_release_summary(
        contractors=contractors,
        environments_map=environments_map,
        platforms=platforms,
        total_commands=len(executed_commands),
    )

    print("📋 Lista de comandos executados:\n")
    for idx, cmd in enumerate(executed_commands, start=1):
        print(f"{idx:02d}. {cmd}")


if __name__ == "__main__":
    main()


