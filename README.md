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

### Kepler

Skills from this repository are available automatically in Kepler.

### Claude Code

```bash
# Via skill source (recommended)
claude skill add https://github.com/michaeljabbour/amplifier-kepler-skill

# Or clone manually
git clone https://github.com/michaeljabbour/amplifier-kepler-skill ~/.amplifier/skill-sources/amplifier-kepler-skill
```

### Other Amplifier Instances

Add to your `tool-skills` configuration:

```yaml
skill_sources:
  - name: amplifier-kepler-skill
    url: https://github.com/michaeljabbour/amplifier-kepler-skill
```

### Other Tools

```bash
git clone https://github.com/michaeljabbour/amplifier-kepler-skill
# Reference the skill files directly in your tool's context
```

## Relationship to Other Skill Repos

```
amplifier-foundation-skills    — Core Amplifier skills (all distributions)
amplifier-kepler-skill         — Kepler-specific skills (this repo)
amplifier-cloud-skill          — Cloud/server deployment skills
```

Foundation skills provide universal Amplifier knowledge. This repository layers
Kepler-specific knowledge on top — Tauri architecture, sidecar patterns,
desktop distribution concerns.

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
