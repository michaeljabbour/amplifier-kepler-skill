# amplifier-kepler-skill

Skills for developing and extending Kepler — the Amplifier desktop distribution.

## Skills Included

| Skill | Description |
|-------|-------------|
| `kepler-architecture` | Kepler system architecture — Tauri, sidecar, IPC patterns |
| `kepler-dev-setup` | Development environment setup and workflow |
| `kepler-sidecar-patterns` | Python sidecar patterns — FastAPI, lifecycle, health checks |
| `kepler-bundle-composition` | Bundle and agent composition patterns for Kepler |

## Install

### Kepler Desktop

Skills from this repository are available automatically in Kepler Desktop
(they're wired into Kepler's `desktop.yaml` bundle config).

### Global Installation (All Amplifier Instances)

To make these skills available to **every** Amplifier instance (CLI, Desktop,
any tool) regardless of which project you're working in, symlink each skill
directory into `~/.amplifier/skills/`:

```bash
# Clone the repo (if you haven't already)
git clone https://github.com/michaeljabbour/amplifier-kepler-skill.git ~/dev/amplifier-kepler-skill

# Create the global skills directory
mkdir -p ~/.amplifier/skills

# Symlink each skill directory
ln -sf ~/dev/amplifier-kepler-skill/kepler-architecture ~/.amplifier/skills/kepler-architecture
ln -sf ~/dev/amplifier-kepler-skill/kepler-dev-setup ~/.amplifier/skills/kepler-dev-setup
ln -sf ~/dev/amplifier-kepler-skill/kepler-sidecar-patterns ~/.amplifier/skills/kepler-sidecar-patterns
ln -sf ~/dev/amplifier-kepler-skill/kepler-bundle-composition ~/.amplifier/skills/kepler-bundle-composition
```

After this, any Amplifier session can run `load_skill("kepler-architecture")`
from any project directory.

### Claude Code

```bash
# Via skill source (recommended)
claude skill add https://github.com/michaeljabbour/amplifier-kepler-skill

# Or clone manually and reference SKILL.md files directly
git clone https://github.com/michaeljabbour/amplifier-kepler-skill ~/.amplifier/skill-sources/amplifier-kepler-skill
```

You can also point Claude Code at individual skill files:
```
Read ~/dev/amplifier-kepler-skill/kepler-architecture/SKILL.md for the
Kepler concentric rings model, then review my proposed change.
```

### Bundle YAML Configuration

Add to your project's bundle YAML to make skills available per-project:

```yaml
tools:
  - module: tool-skills
    config:
      skills_dirs:
        - ~/dev/amplifier-kepler-skill
```

### Other Tools

```bash
git clone https://github.com/michaeljabbour/amplifier-kepler-skill
# Reference the SKILL.md files directly in your tool's context
```

## Relationship to Other Skill Repos

These three skill repositories layer on top of each other:

```
amplifier-skill            — Core Amplifier patterns (delegation, CLI, agents)
amplifier-kepler-skill     — Kepler-specific skills (this repo)
amplifier-tauri-skill      — Generic Tauri 2.0 development skills
```

- **`amplifier-skill`** provides universal Amplifier knowledge: how delegation
  works, CLI discovery, agent catalog, module contracts.
- **`amplifier-kepler-skill`** (this repo) layers Kepler-specific knowledge on
  top: concentric rings architecture, bundle composition, sidecar lifecycle,
  desktop distribution concerns.
- **`amplifier-tauri-skill`** provides generic Tauri 2.0 knowledge: project
  structure, IPC patterns, sidecar integration. Not Kepler-specific -- useful
  for any Tauri app.

To install all three globally:

```bash
mkdir -p ~/.amplifier/skills

# Core Amplifier skill
ln -sf ~/dev/amplifier-skill ~/.amplifier/skills/amplifier-skill

# Kepler skills
ln -sf ~/dev/amplifier-kepler-skill/kepler-architecture ~/.amplifier/skills/kepler-architecture
ln -sf ~/dev/amplifier-kepler-skill/kepler-dev-setup ~/.amplifier/skills/kepler-dev-setup
ln -sf ~/dev/amplifier-kepler-skill/kepler-sidecar-patterns ~/.amplifier/skills/kepler-sidecar-patterns
ln -sf ~/dev/amplifier-kepler-skill/kepler-bundle-composition ~/.amplifier/skills/kepler-bundle-composition

# Tauri skills
ln -sf ~/dev/amplifier-tauri-skill/tauri2-project-structure ~/.amplifier/skills/tauri2-project-structure
ln -sf ~/dev/amplifier-tauri-skill/tauri2-ipc-patterns ~/.amplifier/skills/tauri2-ipc-patterns
ln -sf ~/dev/amplifier-tauri-skill/tauri2-sidecar-integration ~/.amplifier/skills/tauri2-sidecar-integration
```

## Repository Layout

```
.
├── README.md
├── .gitignore
├── test_skills.py
├── kepler-architecture/
│   └── SKILL.md
├── kepler-dev-setup/
│   └── SKILL.md
├── kepler-sidecar-patterns/
│   └── SKILL.md
├── kepler-bundle-composition/
│   └── SKILL.md
└── docs/
    └── cross-tool-skill-discovery.md
```
