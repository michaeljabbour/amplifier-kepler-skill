# Cross-Tool Skill Discovery Guide

How to use Amplifier and Kepler skills across different AI coding tools.

## The Three Skill Repos

| Repo | Scope | When to Use |
|------|-------|-------------|
| `amplifier-skill` | Core Amplifier delegation patterns | Any project that uses Amplifier |
| `amplifier-kepler-skill` | Kepler architecture, sidecar, bundles | Working on or designing for Kepler |
| `amplifier-tauri-skill` | Generic Tauri 2.0 patterns | Any Tauri 2.0 project |

## Designing "the Amplifier Way" + Working with Kepler

Install both `amplifier-skill` and `amplifier-kepler-skill`. The combination
gives your tool:

1. **From `amplifier-skill`:** How to delegate to Amplifier, discover agents,
   query sessions, handle failures
2. **From `amplifier-kepler-skill`:** The concentric rings model, what code
   belongs in which layer, bundle composition rules, sidecar patterns

Together, they teach any AI tool to design features that work correctly within
both the Amplifier ecosystem and the Kepler desktop app.

## Installation by Tool

### Claude Code

```bash
# Install all three for full Kepler development
claude skill add https://github.com/michaeljabbour/amplifier-skill
claude skill add https://github.com/michaeljabbour/amplifier-kepler-skill
claude skill add https://github.com/michaeljabbour/amplifier-tauri-skill
```

Skills appear in Claude Code's `/skill` command and are auto-discovered
when relevant to the conversation.

### Kepler (built-in)

Kepler pre-configures the skill repos in `desktop.yaml`. Every agent session
discovers them automatically via the `tool-skills` module. No manual install needed.

### Other Amplifier Instances (CLI, other distros)

Add to your bundle YAML or `~/.amplifier/config.yaml`:

```yaml
tools:
  - module: tool-skills
    config:
      skills_dirs:
        - ~/dev/amplifier-kepler-skill
        - ~/dev/amplifier-tauri-skill
```

Or import via the Amplifier skill import mechanism:

```bash
amplifier skill import git+https://github.com/michaeljabbour/amplifier-kepler-skill@main
```

### Warp / Cursor / Other Tools

Clone the repos and point your tool's skill/command directory:

```bash
# Clone to a shared skills location
git clone https://github.com/michaeljabbour/amplifier-skill ~/skills/amplifier
git clone https://github.com/michaeljabbour/amplifier-kepler-skill ~/skills/kepler
git clone https://github.com/michaeljabbour/amplifier-tauri-skill ~/skills/tauri
```

Then configure your tool to scan `~/skills/` for skill definitions.

### Manual / Generic

Each skill is a standalone `SKILL.md` file in a named directory. Copy the
directories you need into wherever your tool looks for skills/prompts:

```bash
# Just the architecture skill
cp -r amplifier-kepler-skill/kepler-architecture/ ~/.my-tool/skills/

# All kepler skills
cp -r amplifier-kepler-skill/*/ ~/.my-tool/skills/
```

## Combining Skills

Skills are designed to layer:

```
amplifier-skill                 (base: delegation patterns)
  + amplifier-kepler-skill      (adds: Kepler architecture knowledge)
  + amplifier-tauri-skill        (adds: Tauri 2.0 generic patterns)
```

You can use any combination:
- **`amplifier-skill` alone** — for pure Amplifier CLI/delegation work
- **`amplifier-skill` + `kepler-skill`** — for Kepler sidecar/backend work
- **`amplifier-skill` + `kepler-skill` + `tauri-skill`** — for full-stack Kepler work
- **`tauri-skill` alone** — for any Tauri 2.0 project, no Amplifier needed

## Creating Your Own Skills

Use `amplifier-skill` as the template:

1. Create a directory with a `SKILL.md` file
2. Add YAML frontmatter: `name` and `description` (required)
3. Write actionable markdown: workflows, patterns, guardrails
4. Keep it focused — one skill = one domain of expertise
5. Put it in a git repo for distribution

See [github.com/michaeljabbour/amplifier-skill](https://github.com/michaeljabbour/amplifier-skill)
for the canonical example.
