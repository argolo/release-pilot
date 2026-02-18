# Contributing to ReleasePilot

First of all, thank you for your interest in contributing to **ReleasePilot** ❤️
Contributions of all kinds are welcome: ideas, documentation, bug reports, improvements, and code.

This document defines **clear guidelines** to ensure that contributions remain aligned with the project’s philosophy, quality standards, and long-term vision.

---

## 🧭 Project Philosophy

ReleasePilot is **not** a generic automation tool.

Its core principles are:

* **Orchestration over automation**
* **Deterministic execution**
* **Human-in-the-loop control**
* **Clear separation of responsibilities**

ReleasePilot orchestrates commands — it does **not** implement low-level build logic.
Platform-specific, contractor-specific, or environment-specific logic **must live in `yarn` scripts**, not inside the orchestrator.

When contributing, always ask:

> *Does this change improve orchestration, clarity, safety, or predictability?*

If the answer is “no”, the contribution may not be accepted.

---

## 📦 Scope of Contributions

### ✅ Good candidates for contributions

* Improvements to orchestration logic
* CLI UX enhancements (flags, output clarity, validation)
* Documentation improvements
* Bug fixes
* Test coverage
* CI/CD improvements
* Cross-platform compatibility
* Developer experience (DX) improvements

### ❌ Out of scope

* Embedding build logic inside ReleasePilot
* Adding platform-specific or contractor-specific workflows
* Introducing heavy external dependencies
* Automating steps that intentionally require human confirmation
* Breaking the interactive flow without a clear alternative (e.g. `--ci`)

---

## 🛠️ Development Setup

### Requirements

* Python **3.9+**
* Node.js + Yarn
* Git

### Clone the repository

```bash
git clone https://github.com/<your-org>/release-pilot.git
cd release-pilot
```

### Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install in editable mode

```bash
pip install -e .
```

Or, if you are working on the CLI behavior:

```bash
pipx install . --force
```

---

## ▶️ Running the Project Locally

From the project root:

```bash
release-pilot
```

Make sure you are inside a directory that follows the expected structure:

```text
contractor/
  └─ example/
     └─ sandbox/
```

---

## 🧪 Testing

ReleasePilot aims to be **predictable and safe**.

When adding or modifying code:

* Prefer **pure functions** where possible
* Avoid executing real `yarn` commands in tests
* Use mocking for subprocess calls
* Keep tests deterministic

If you introduce new behavior, **tests are strongly encouraged**.

---

## 🎨 Code Style & Conventions

* Follow **PEP 8**
* Use **type hints** consistently
* Prefer explicit code over clever code
* Keep functions small and focused
* Use docstrings for all public functions
* Keep messages and CLI output **in English**
* Do not introduce external dependencies without strong justification

ReleasePilot intentionally avoids frameworks and heavy abstractions.

---

## 🔀 Branching & Workflow

* Base branch: `main`
* Create feature branches from `main`
* Use descriptive branch names:

```text
feature/add-dry-run
fix/ci-non-interactive
docs/improve-readme
```

---

## 📬 Submitting a Pull Request

Before submitting a PR, ensure that:

* [ ] The code builds and runs locally
* [ ] The CLI behaves as documented
* [ ] Existing behavior is not broken
* [ ] New behavior is documented
* [ ] Code is readable and maintainable
* [ ] Tests are added or updated (when applicable)

### Pull Request Description

Please include:

* **What** is being changed
* **Why** the change is necessary
* **How** it aligns with ReleasePilot’s philosophy
* Any relevant screenshots or logs (if applicable)

Low-context PRs are likely to be rejected.

---

## 🐛 Reporting Bugs

If you find a bug, please open an issue and include:

* Clear description of the problem
* Steps to reproduce
* Expected vs actual behavior
* Environment details (OS, Python version)
* Relevant logs or output

---

## 💡 Feature Requests

Feature requests are welcome, but please keep in mind:

* ReleasePilot prioritizes **clarity and safety**
* Not every automation belongs in the orchestrator
* Simplicity is a feature

Well-argued proposals have a much higher chance of acceptance.

---

## 📜 Code of Conduct

This project follows the **Contributor Covenant Code of Conduct**.

By participating, you agree to uphold a respectful, inclusive, and professional environment.

---

## 🙏 Final Notes

ReleasePilot is built to serve **real-world, high-responsibility release workflows**.
Quality, predictability, and trust are more important than speed or novelty.

Thank you for helping make ReleasePilot better 🚀
