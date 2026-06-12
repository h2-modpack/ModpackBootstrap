# {{WINDOW_TITLE}} Modpack

Shell repo for the {{WINDOW_TITLE}} modpack. Contains the coordinator, shared Lib submodule, ModpackTools, and the game-module submodules for this pack.

## Structure

```text
{{SHELL_REPO}}/
|- {{COORD_ID}}/              # Coordinator: pack identity, config, profiles
|- adamant-ModpackLib/        # Shared module and modpack runtime
|- ModpackTools/              # Pack maintenance scripts
'- Submodules/                # Game modules (one repo each)
```

## Local Development

```bash
git clone --recurse-submodules https://github.com/{{ORG}}/{{SHELL_REPO}}.git
ModpackTools/run ModpackTools/local_deploy/deploy_all.py
```

For the full new-pack workflow, use
[ModpackBootstrap Getting Started](https://github.com/h2-modpack/ModpackBootstrap/blob/main/docs/GETTING_STARTED.md).

## Releasing

Use the **Release All** workflow (`Actions -> Release All`) to publish a new version across all modules.

## Shared Docs

Use the stable repo-root entrypoints for shared docs:

- [ModpackLib README.md](https://github.com/h2-modpack/adamant-ModpackLib/blob/main/README.md)
- [Hot Reload Architecture](https://github.com/h2-modpack/adamant-ModpackLib/blob/main/docs/lib-contributors/HOT_RELOAD_ARCHITECTURE.md)
- [Known Limitations](https://github.com/h2-modpack/adamant-ModpackLib/blob/main/docs/references/KNOWN_LIMITATIONS.md)

This shell repo should only document pack-specific structure and composition.
