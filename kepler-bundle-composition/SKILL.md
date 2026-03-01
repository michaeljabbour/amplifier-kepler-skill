---
name: kepler-bundle-composition
description: Bundle composition with desktop.yaml — Ring 3 vs Ring 4 boundaries and patterns
---

# Kepler Bundle Composition

Kepler's identity is defined by `desktop.yaml` — the Ring 3 distribution composition file. It declares which bundles, providers, tools, and hooks make up the Kepler experience.

## desktop.yaml Structure

```yaml
bundle:
  name: kepler-desktop
  version: "1.0.0"
  description: Amplifier desktop distribution

includes:
  # Ring 2 foundation bundles
  - "@foundation:core"
  - "@foundation:tools/file-ops"
  - "@foundation:tools/shell"
  - "@foundation:tools/web"
  - "@foundation:agents/delegation"

  # Ring 3 Kepler-specific bundles
  - "@kepler:desktop-tools"
  - "@kepler:approval-hooks"

context:
  # System context assembled from multiple sources
  - source: "@foundation:context/system"
  - source: "@kepler:context/desktop"
  - source: user://~/.kepler/context.md

providers:
  anthropic:
    models:
      - claude-sonnet-4-20250514
      - claude-haiku-4-20250514
    default: claude-sonnet-4-20250514
  openai:
    models:
      - gpt-4o
      - gpt-4o-mini

tools:
  file_ops:
    approval: required
  shell:
    approval: required
    timeout: 30
  web_fetch:
    approval: auto
  web_search:
    approval: auto

hooks:
  pre_tool:
    - "@kepler:hooks/approval-gate"
    - "@kepler:hooks/audit-log"
  post_turn:
    - "@kepler:hooks/usage-tracker"
  on_error:
    - "@kepler:hooks/error-reporter"
```

## What Belongs Where

### Ring 3 — Distribution Config (`desktop.yaml`)

Ring 3 is **pure composition**. It contains:

- Which bundles to include
- Which providers to configure
- How tools are wired (approval levels, timeouts)
- Which hooks run at each lifecycle point
- Context assembly order

Ring 3 should **never contain code**. If you're writing Python, Rust, or TypeScript, it belongs in Ring 2 (foundation) or Ring 4 (desktop app).

### Ring 4 — Desktop App Code

Ring 4 contains **implementation** that requires the desktop runtime:

- Tauri native shell (Rust)
- Python sidecar (FastAPI routes, services)
- Frontend components (TypeScript/React)
- IPC bridge between frontend and sidecar
- Desktop-specific hooks (approval UI, notifications)

If the code could work outside a desktop context, it probably belongs in Ring 2 instead.

## Adding a New Bundle

1. **Create the bundle** in the appropriate ring:
   - Ring 2: Add to `amplifier-foundation` if it's reusable across distributions
   - Ring 3: Add to `amplifier-distro-kepler` as a Kepler-specific bundle
   - Ring 4: Add as part of the desktop app implementation

2. **Register in desktop.yaml** under the `includes:` section:
   ```yaml
   includes:
     - "@foundation:my-new-bundle"    # Ring 2
     - "@kepler:my-desktop-bundle"    # Ring 3
   ```

3. **Wire configuration** if the bundle needs tool config or hooks:
   ```yaml
   tools:
     my_new_tool:
       approval: required
   hooks:
     pre_tool:
       - "@kepler:hooks/my-new-hook"
   ```

4. **Test the composition** by running Kepler in dev mode and verifying the bundle loads:
   ```bash
   npm run tauri dev
   # Check sidecar logs for bundle registration
   ```

## Adding a New Provider

Add a provider entry to the `providers:` section:

```yaml
providers:
  anthropic:
    models:
      - claude-sonnet-4-20250514
    default: claude-sonnet-4-20250514
  my-new-provider:
    models:
      - model-name-v1
      - model-name-v2
    default: model-name-v1
    api_base: https://api.my-provider.com/v1
```

The provider must implement the Amplifier Core provider protocol (Ring 1). The `desktop.yaml` only declares which providers are available and how they're configured — it does not implement the provider itself.

## Composition Rules

These 5 rules govern how Kepler bundles are composed:

1. **Inner rings never reference outer rings.** Ring 1 cannot import from Ring 2. Ring 2 cannot reference Ring 3 config. Dependencies flow inward only.

2. **desktop.yaml is the single source of truth.** All bundle inclusion, provider wiring, and hook configuration lives in `desktop.yaml`. No implicit registration.

3. **Bundles must be self-contained.** A bundle declares its own tools, context, and dependencies. It does not reach into other bundles at runtime.

4. **User config (Ring 5) overrides distribution config (Ring 3).** Settings in `~/.kepler/settings.yaml` take precedence over `desktop.yaml` defaults. Users always win.

5. **Composition is additive, not destructive.** Adding a bundle should never break existing bundles. If bundles conflict, the composition is invalid — fix it, don't work around it.
