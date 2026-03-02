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

### Quick Install (Amplifier + Claude Code)

```bash
git clone https://github.com/michaeljabbour/amplifier-kepler-skill.git ~/dev/amplifier-kepler-skill
cd ~/dev/amplifier-kepler-skill
./install.sh
```

This creates symlinks in both `~/.amplifier/skills/` and `~/.claude/skills/`,
so every Amplifier session and every Claude Code session sees the same skills.
Update anytime with `git pull` — symlinks mean both tools pick up changes
instantly.

### Amplifier Bundle YAML (alternative)

If you prefer git-sourced skills fetched on the fly:

```yaml
tools:
  - module: tool-skills
    config:
      skills:
        - "git+https://github.com/michaeljabbour/amplifier-kepler-skill@main"
```

### Kepler Desktop

Already configured via `behaviors/skills.yaml`. Nothing to install.

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
