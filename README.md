# 🚀 ReleasePilot — Deterministic orchestration of white-label app builds

[![CI](https://github.com/argolo/release-pilot/actions/workflows/ci.yml/badge.svg)](https://github.com/argolo/release-pilot/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/argolo/release-pilot)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/argolo/release-pilot)](https://github.com/argolo/release-pilot/commits/main)
[![Open Issues](https://img.shields.io/github/issues/argolo/release-pilot)](https://github.com/argolo/release-pilot/issues)

[![PyPI Version](https://img.shields.io/pypi/v/release-pilot.svg)](https://pypi.org/project/release-pilot/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/release-pilot.svg)](https://pypi.org/project/release-pilot/)
[![PyPI](https://badge.fury.io/py/release-pilot.svg)](https://pypi.org/project/release-pilot/)


**ReleasePilot** is an **assisted release orchestrator** that executes `yarn` commands in an **organized, deterministic, and controlled** manner, based on variables provided by the operator (platform, contractor, environment, and command).

Its primary goal is to **standardize and automate the build, packaging, and delivery process of white-label applications**, while respecting the specific differences between contractors, environments, and platforms — without sacrificing **human control at critical steps**.

ReleasePilot is intentionally designed to **orchestrate** commands, not to encapsulate low-level logic or highly specific operational flows. For this reason, granular commands, deep customizations, or platform-specific behaviors **must live in dedicated build flows**, which are then invoked by `yarn`.

The orchestrator’s responsibility is to **order, coordinate, and operate** these commands in a consistent, predictable, and auditable way. To enable this, the `package.json` must define **script aliases** that follow the ReleasePilot convention:

```
{platform}:{contractor}:{environment}:{command}
```

This allows `yarn` to act as the execution layer, while ReleasePilot acts as the orchestration layer.

---

## 🎯 Purpose

ReleasePilot was created to solve a recurring problem in white-label ecosystems:

> **How can we execute multiple build commands in a consistent, predictable, and auditable way when each application varies by contractor, environment, and platform?**

The answer is not blind automation — it is **conscious orchestration**.

---

## ✨ Key Features

* 🎛️ Orchestration of `yarn` commands based on operational variables
* 📱 Multi-platform support (`android`, `ios`)
* 🏢 Automatic discovery of **contractors** via directory structure
* 🧪 Automatic discovery of **environments** per contractor
* ⚙️ Supported commands: `add`, `build`, `deploy`
* 🔁 **“All”** option available in every selection step
* ⏸️ **Assisted execution** with human checkpoints between:

  * Environments
  * Contractors
* 📌 Execution planning **identical to the real execution order**
* 📦 Final, traceable release summary
* 🧩 Simple, pythonic code with **no external dependencies**

---

## 🧠 Operational Philosophy

ReleasePilot **does not execute commands randomly**.

It:

* Organizes
* Orders
* Operates

Each `yarn` command is executed within a **well-defined context**, ensuring that:

* Builds are not mixed across contractors
* Environments are strictly respected
* Artifacts can be safely retrieved between steps
* The operator has full visibility into what is being executed

---

## 📂 Expected Project Structure

```text
project-root/
├─ contractor/
│  ├─ quickup/
│  │  ├─ sandbox/
│  │  ├─ alfa/
│  │  └─ beta/
│  ├─ kompa/
│     ├─ sandbox/
│     ├─ beta/
│     └─ prod/
```

> The project name is automatically inferred from the **root directory name**.

---

## 🧾 Command Pattern

ReleasePilot executes commands following this convention:

```bash
yarn {platform}:{contractor}:{environment}:{command}
```

### Example

```bash
yarn android:quickup:beta:build
```

---

## 🚀 Installation

### Requirements

* Python **3.9+**
* Node.js + Yarn
* Git (optional, but recommended for traceability)


### 3️⃣ Install ReleasePilot globally

```bash
pip3 install release-pilot
```

The command will now be available globally as:

```bash
release-pilot
```

---

### ▶️ Quick Test

```bash
release-pilot
```

If the interactive menu appears, the installation was successful ✅

---

### 🔍 Optional Checks

```bash
which release-pilot
pip list
```

Expected output (example):

```text
~/.local/bin/release-pilot
```

---

### ❌ Uninstalling

```bash
pip3 uninstall release-pilot
```

---

### ⚠️ Important Notes for macOS

* **Do not use `sudo pip install`**
* **Do not use the system Python to install CLIs**
* **Do not manually copy binaries**
* For Python CLI tools, **pipx is always the correct choice**

---

### 🧠 Rule of Thumb

> **Python library → `pip install`**

---

## 📌 Execution Planning

Before executing any command, ReleasePilot displays the **complete execution plan**, in the **exact order in which commands will run**.

This eliminates ambiguity and ensures full predictability.

---

## ✅ Final Release Summary

At the end of execution, ReleasePilot presents a consolidated summary including:

* 📁 Project
* 📦 Contractors
* 🌿 Git branch / version
* 🧪 Environments
* 📱 Platforms
* ⚙️ Total executed commands

This summary improves auditability, communication, and release traceability.

---

## 🛡️ Ideal Use Cases

* White-label app builds
* Sandbox / alfa / beta / production environments
* Teams supporting multiple clients
* Sensitive or regulated releases
* Teams that require **control + automation**

---

## 🔮 Future Enhancements

* `--dry-run` mode
* Non-interactive execution (`--ci`)
* Summary export (`.txt` / `.md`)
* Commit hash and SemVer tag support
* Slack / Jira / Discord / Telegram integrations
* Persistent execution logs

---

## 📜 License

MIT License.

---

## 👤 Author

**André Argôlo**
CTO • Software Architect • DevOps

* 🌐 Website: [https://argolo.dev](https://argolo.dev)
* 🐙 GitHub: [@argolo](https://github.com/argolo)

---

### 🧭 About

André Argôlo is a software architect and technology leader with extensive experience in designing and operating mission-critical systems. His work focuses on building scalable platforms, improving developer experience, and creating pragmatic tooling that balances automation with human control — especially in regulated and high-responsibility environments.

