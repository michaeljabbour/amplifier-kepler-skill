---
name: kepler-architecture
description: Kepler system architecture — the concentric rings model for desktop AI distribution
---

# Kepler Architecture

Kepler is the Amplifier desktop distribution. Its architecture follows a **concentric rings model** where each ring has clear responsibilities, ownership boundaries, and dependency rules.

## The Five Rings

```
┌─────────────────────────────────────────────┐
│              Ring 5 · User Layer             │
│  ┌─────────────────────────────────────────┐ │
│  │         Ring 4 · Desktop App            │ │
│  │  ┌───────────────────────────────────┐  │ │
│  │  │      Ring 3 · Distribution        │  │ │
│  │  │  ┌─────────────────────────────┐  │  │ │
│  │  │  │    Ring 2 · Foundation      │  │  │ │
│  │  │  │  ┌───────────────────────┐  │  │  │ │
│  │  │  │  │  Ring 1 · Amp Core   │  │  │  │ │
│  │  │  │  └───────────────────────┘  │  │  │ │
│  │  │  └─────────────────────────────┘  │  │ │
│  │  └───────────────────────────────────┘  │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

- **Ring 1 — Amplifier Core**: The kernel. Agent loop, provider protocol, tool dispatch, module contracts. Zero distribution knowledge.
- **Ring 2 — Foundation**: Bundles, skills, behaviors, context modules. Distribution-agnostic building blocks.
- **Ring 3 — Distribution (Kepler Config)**: `desktop.yaml` bundle composition, provider wiring, hook configuration. What makes Kepler *Kepler*.
- **Ring 4 — Desktop App**: Tauri shell, Electron/webview, sidecar process management, IPC bridge, native capabilities.
- **Ring 5 — User Layer**: User settings, custom bundles, personal preferences, workspace overrides.

## Ring Responsibilities

### Ring 1 — Amplifier Core

| Repo | Provides |
|------|----------|
| `amplifier-core` | Agent loop, provider protocol, tool dispatch |
| `amplifier-core` | Module contracts (Provider, Tool, Hook, Context) |
| `amplifier-core` | Session lifecycle, event system |

Ring 1 has **zero knowledge** of any distribution. It defines protocols — not implementations.

### Ring 2 — Foundation

| Repo | Provides |
|------|----------|
| `amplifier-foundation` | Bundle system, skill loader, behavior modules |
| `amplifier-foundation` | Standard tools (file ops, shell, web) |
| `amplifier-foundation` | Agent delegation framework |

Ring 2 builds reusable blocks. It does not know about Tauri, Electron, or desktop concerns.

### Ring 3 — Distribution

| Repo | Provides |
|------|----------|
| `amplifier-distro-kepler` | `desktop.yaml` — the bundle composition file |
| `amplifier-distro-kepler` | Provider configuration and wiring |
| `amplifier-distro-kepler` | Hook chains and context assembly |

Ring 3 is **configuration, not code**. It composes Ring 2 blocks into the Kepler experience.

### Ring 4 — Desktop App

| Repo | Provides |
|------|----------|
| `amplifier-distro-kepler` | Tauri native shell and window management |
| `amplifier-distro-kepler` | Python sidecar (FastAPI) |
| `amplifier-distro-kepler` | IPC bridge between frontend and sidecar |
| `amplifier-distro-kepler` | Native file dialogs, system tray, notifications |

Ring 4 is the **application layer** — everything specific to running on a desktop OS.

### Ring 5 — User Layer

| Repo | Provides |
|------|----------|
| User's machine | `~/.kepler/settings.yaml` preferences |
| User's machine | Custom bundles and overrides |
| User's machine | Workspace-level configuration |

Ring 5 is never checked into any repo. It belongs to the user.

## Decision Checklist

Use these questions to determine where code belongs:

1. **Does it define a protocol or contract?** → Ring 1 (amplifier-core)
2. **Is it a reusable building block with no desktop dependency?** → Ring 2 (amplifier-foundation)
3. **Does it compose existing blocks into a distribution?** → Ring 3 (desktop.yaml config)
4. **Does it require native OS capabilities or desktop runtime?** → Ring 4 (Tauri/sidecar)
5. **Is it a user preference or personal customization?** → Ring 5 (user config)

If you're unsure, start at Ring 1 and work outward. Code should live at the **innermost ring** that makes sense — inner rings are more reusable.

## Kepler Repo Structure

```
amplifier-distro-kepler/
├── desktop.yaml                 # Ring 3 — distribution composition
├── sidecar/                     # Ring 4 — Python sidecar
│   ├── main.py                  #   FastAPI app entry
│   ├── routes/                  #   API route modules
│   │   ├── agent.py             #     Agent spawn/stream endpoints
│   │   ├── session.py           #     Session management
│   │   └── tools.py             #     Tool execution
│   ├── services/                #   Business logic
│   │   ├── agent_service.py     #     Agent lifecycle
│   │   └── approval.py          #     Desktop approval system
│   └── pyproject.toml           #   Python dependencies
├── src/                         # Ring 4 — Frontend (TypeScript)
│   ├── App.tsx                  #   Main app component
│   ├── components/              #   UI components
│   └── lib/                     #   Frontend utilities
├── src-tauri/                   # Ring 4 — Tauri native shell (Rust)
│   ├── src/
│   │   └── main.rs              #   Tauri entry point
│   ├── Cargo.toml               #   Rust dependencies
│   └── tauri.conf.json          #   Tauri configuration
├── docs/                        # Documentation
│   └── architecture.md          #   Canonical architecture reference
└── tests/                       # Test suites
    ├── sidecar/                 #   Python sidecar tests
    └── frontend/                #   Frontend tests
```

## Canonical Reference

The full canonical architecture guide lives at:

```
amplifier-distro-kepler/docs/architecture.md
```

This skill provides a working summary. For exhaustive detail — including IPC message formats, sidecar lifecycle diagrams, and deployment topology — consult the canonical reference in the Kepler repo.
