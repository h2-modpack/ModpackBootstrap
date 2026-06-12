# Getting Started

This is the shortest path from no pack to a local Hades II modpack workspace
with one editable module.

## What You Are Creating

The stack is split into a few repos:

| Repo | Role |
| --- | --- |
| shell repo | Owns the pack workspace and submodule pointers |
| coordinator repo | Owns pack identity, profiles, module order, and shared menu bootstrap |
| `adamant-ModpackLib` | Shared module runtime contract |
| `ModpackTools` | Ongoing pack maintenance, module creation, local deploy, and release helpers |
| module repos | One repo per gameplay/UI module under `Submodules/` |

`ModpackBootstrap` is used once to create the shell and coordinator. After that,
work from inside the generated shell repo with `ModpackTools`.

## Prerequisites

- Python 3.11+
- Git
- GitHub CLI authenticated with repo creation permission
- r2modman with a Hades II profile for local deployment

Release publishing also needs GitHub Actions org secrets:

- `TCLI_AUTH_TOKEN`
- `RELEASE_DISPATCH_TOKEN`

## 1. Create The Pack

Clone Bootstrap next to where the new shell folder should live:

```bash
git clone https://github.com/h2-modpack/ModpackBootstrap.git
python ModpackBootstrap/new_pack.py \
  --pack-id speedrun \
  --pack-name "Speedrun" \
  --coordinator-package Speedrun_Modpack \
  --team adamantSpeedrun \
  --org h2pack-speedrun
```

Naming rules:

- `--pack-id` is the internal modpack id and shell repo slug. The shell repo
  and local folder become `{pack-id}-modpack`.
- `--pack-name` is the in-game display name.
- `--coordinator-package` is the coordinator Thunderstore package suffix.
- `--team` is the Thunderstore team/namespace for pack-owned packages.
- `--org` is the GitHub org where pack repos are created.

The script prints the exact repos, folders, package names, and side effects
before it creates anything.

## 2. Deploy The Empty Pack

From the generated shell repo:

```bash
cd speedrun-modpack
ModpackTools/run ModpackTools/local_deploy/deploy_all.py --overwrite
```

Local deploy stages package assets, generates manifests, links packages into the
r2modman profile, and installs git hooks.

## 3. Add A Module

From the shell repo root:

```bash
ModpackTools/run ModpackTools/new_module/create.py --package-id My_Module --title "My Module"
ModpackTools/run ModpackTools/local_deploy/deploy_all.py --overwrite
```

The module creator scaffolds from
[`ModpackModuleTemplate`](https://github.com/h2-modpack/ModpackModuleTemplate),
creates the GitHub repo, clones it under `Submodules/`, and syncs the
coordinator dependency block.

Module package names use the pack team as the namespace. For example, with
`--team adamantSpeedrun`, `--package-id LiveSplit` creates
`adamantSpeedrun-LiveSplit`.

## 4. Edit The Module

Start with these files in the new module repo:

| File | Owns |
| --- | --- |
| `src/main.lua` | module creation, capability declarations, fallback UI, activation |
| `src/mods/data.lua` | storage schema, static option lists, lookup data |
| `src/mods/ui.lua` | module tab and quick-content draw callbacks |
| `src/mods/logic.lua` | hooks, mutations, and runtime behavior |

Typical flow:

1. Add settings in `src/mods/data.lua`.
2. Draw those settings in `src/mods/ui.lua`.
3. Register hooks or mutations in `src/mods/logic.lua`.
4. Keep `src/main.lua` as the entrypoint that wires the pieces together.

## 5. Validate

From the shell repo root:

```bash
ModpackTools/run ModpackTools/test_all.py
```

For a faster tools-only check:

```bash
ModpackTools/run ModpackTools/test_all.py --python-only
```

## 6. Release

After module/coordinator changes are committed and pushed, commit the shell
submodule pointers. Then run the shell repo's **Release All** GitHub Actions
workflow.

Release All validates the checked-out shell snapshot, checks platform dependency
edges, and dispatches release workflows for the selected packages.

## Where To Read Next

- [`ModpackTools` README](https://github.com/h2-modpack/ModpackTools/blob/main/README.md)
  for module creation, local deploy, release, and maintenance commands.
- [`ModpackModuleTemplate` README](https://github.com/h2-modpack/ModpackModuleTemplate/blob/main/README.md)
  for the default module file layout.
- [`ModpackLib` module author docs](https://github.com/h2-modpack/adamant-ModpackLib/blob/main/docs/module-authors/GETTING_STARTED.md)
  for the module runtime contract.
