# amplifier-kepler-skill

Skills for developing and extending [Kepler](https://github.com/michaeljabbour/amplifier-distro-kepler) -- the Amplifier desktop distribution. These skills teach AI coding assistants the Kepler concentric rings architecture, sidecar patterns, bundle composition rules, and dev environment setup.

## Skills Included

| Skill | Description |
|-------|-------------|
| `kepler-architecture` | Concentric rings model, layer responsibilities, what belongs where |
| `kepler-dev-setup` | Dev environment: sidecar, Tauri, frontend, linking local amplifier |
| `kepler-sidecar-patterns` | Route structure, spawn capability, streaming, approval protocols |
| `kepler-bundle-composition` | How `desktop.yaml` works, Ring 3 vs Ring 4, adding bundles |

## Install from GitHub

### Amplifier (CLI or Desktop)

**Option A -- Git skill source (recommended, survives updates):**

Add to your bundle YAML or `desktop.yaml`:

```yaml
tools:
  - module: tool-skills
    config:
      skills:
        - "git+https://github.com/michaeljabbour/amplifier-kepler-skill@main"
```

Skills are fetched from GitHub automatically. This config lives in your bundle
file, not in the Amplifier cache, so it survives `amplifier update`.

**Option B -- Clone and symlink for global access:**

```bash
# 1. Clone
git clone https://github.com/michaeljabbour/amplifier-kepler-skill.git ~/dev/amplifier-kepler-skill

# 2. Install into ~/.amplifier/skills/ (survives all updates)
mkdir -p ~/.amplifier/skills
for skill in kepler-architecture kepler-dev-setup kepler-sidecar-patterns kepler-bundle-composition; do
  mkdir -p ~/.amplifier/skills/$skill
  ln -sf ~/dev/amplifier-kepler-skill/$skill/SKILL.md ~/.amplifier/skills/$skill/SKILL.md
done
```

Now any Amplifier session can `load_skill("kepler-architecture")` from any
project. Update skills anytime with `cd ~/dev/amplifier-kepler-skill && git pull`.

> **Why file symlinks?** `pathlib.glob("**")` doesn't follow symlinked
> directories, but follows file symlinks fine.

### Kepler Desktop

Already configured -- skills are wired into Kepler's `desktop.yaml` via the
`behaviors/skills.yaml` behavior bundle. Nothing to install.

### Claude Code

```bash
claude skill add https://github.com/michaeljabbour/amplifier-kepler-skill
```

Or reference individual skills directly:

```
Read ~/dev/amplifier-kepler-skill/kepler-architecture/SKILL.md for the
Kepler concentric rings model, then review my proposed change.
```

### Other Tools (Cursor, Warp, etc.)

```bash
git clone https://github.com/michaeljabbour/amplifier-kepler-skill.git
```

Point your tool at the `SKILL.md` files in each subdirectory.

## Related Skill Repos

These three repos layer on top of each other:

```
amplifier-skill            -- Core Amplifier patterns (delegation, CLI, agents)
amplifier-kepler-skill     -- Kepler-specific (this repo)
amplifier-tauri-skill      -- Generic Tauri 2.0 (project structure, IPC, sidecars)
```

Install all three for full-stack Kepler development:

```yaml
# In your bundle YAML (git sources -- always up to date)
tools:
  - module: tool-skills
    config:
      skills:
        - "git+https://github.com/michaeljabbour/amplifier-skill@main"
        - "git+https://github.com/michaeljabbour/amplifier-kepler-skill@main"
        - "git+https://github.com/michaeljabbour/amplifier-tauri-skill@main"
```

Or clone and symlink all three globally:

```bash
mkdir -p ~/.amplifier/skills

# amplifier-skill (single skill at repo root)
mkdir -p ~/.amplifier/skills/amplifier-skill
ln -sf ~/dev/amplifier-skill/SKILL.md ~/.amplifier/skills/amplifier-skill/SKILL.md

# kepler skills (4 skills)
for skill in kepler-architecture kepler-dev-setup kepler-sidecar-patterns kepler-bundle-composition; do
  mkdir -p ~/.amplifier/skills/$skill
  ln -sf ~/dev/amplifier-kepler-skill/$skill/SKILL.md ~/.amplifier/skills/$skill/SKILL.md
done

# tauri skills (3 skills)
for skill in tauri2-project-structure tauri2-ipc-patterns tauri2-sidecar-integration; do
  mkdir -p ~/.amplifier/skills/$skill
  ln -sf ~/dev/amplifier-tauri-skill/$skill/SKILL.md ~/.amplifier/skills/$skill/SKILL.md
done
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
