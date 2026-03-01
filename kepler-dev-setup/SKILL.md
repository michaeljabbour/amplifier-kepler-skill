---
name: kepler-dev-setup
description: Development environment setup and workflow for Kepler desktop app
---

# Kepler Dev Setup

Complete guide to setting up and running the Kepler development environment.

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python 3.11+ | 3.11 or newer | Sidecar runtime |
| uv | Latest | Python package management |
| Rust | Stable | Tauri native shell |
| cargo | (with Rust) | Rust build system |
| Node 18+ | 18 or newer | Frontend build tooling |
| npm | (with Node) | JavaScript package management |
| Git | Latest | Version control |

Verify prerequisites:

```bash
python3 --version   # 3.11+
uv --version        # any recent
rustc --version     # stable
cargo --version     # comes with Rust
node --version      # 18+
npm --version       # comes with Node
git --version       # any recent
```

## 1. Clone and Setup Sidecar

```bash
git clone https://github.com/michaeljabbour/amplifier-distro-kepler.git
cd amplifier-distro-kepler/sidecar

# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"
```

## 2. Link Local Amplifier

If developing against a local amplifier-core or amplifier-foundation:

```bash
# From the sidecar directory
uv pip install -e /path/to/amplifier-core
uv pip install -e /path/to/amplifier-foundation
```

This ensures sidecar picks up your local changes instead of published packages.

## 3. Setup Tauri Native Shell

```bash
cd src-tauri
cargo build
```

First build downloads and compiles Rust dependencies. Subsequent builds are incremental.

## 4. Setup Frontend

```bash
cd src  # or project root depending on layout
npm install
npm run build  # verify build works
```

## 5. Run Dev Mode

```bash
# From project root — starts Tauri, sidecar, and frontend together
npm run tauri dev
```

This launches:
- Tauri native window
- Python sidecar (auto-spawned)
- Frontend dev server with hot reload

## 6. Run Sidecar Standalone

For sidecar-only development (no Tauri/frontend):

```bash
cd sidecar
uv run python -m main --port 8321 --dev
```

Useful for testing API routes, debugging agent behavior, or running without the desktop shell.

## 7. Run Tests

```bash
# Sidecar tests
cd sidecar
uv run pytest tests/ -v

# Frontend tests
npm test

# Rust/Tauri tests
cd src-tauri
cargo test
```

## Key Files

| File | Purpose |
|------|---------|
| `desktop.yaml` | Bundle composition — defines what Kepler includes |
| `sidecar/main.py` | Sidecar entry point — FastAPI app |
| `sidecar/pyproject.toml` | Python dependencies and project metadata |
| `src-tauri/tauri.conf.json` | Tauri window config, permissions, bundling |
| `src-tauri/Cargo.toml` | Rust dependencies |
| `package.json` | Frontend dependencies and scripts |
| `docs/architecture.md` | Canonical architecture reference |

## Configuration

User-level configuration lives at `~/.kepler/settings.yaml`:

```yaml
# ~/.kepler/settings.yaml
providers:
  default: anthropic
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
  openai:
    api_key: ${OPENAI_API_KEY}

preferences:
  theme: dark
  auto_approve: false
  default_model: claude-sonnet

sidecar:
  port: 8321
  log_level: info
```

Settings are loaded at startup. Changes require restart unless hot-reload is supported for the specific setting.

Environment variables can be referenced with `${VAR_NAME}` syntax. API keys should always use environment variables rather than literal values.
