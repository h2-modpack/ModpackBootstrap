# ModpackBootstrap

One-time bootstrapper for creating a Hades II modpack workspace.

Use this repo to create a new shell repo and coordinator repo. The generated
shell installs `ModpackTools/` as the ongoing pack toolbelt for module
scaffolding, deployment, release orchestration, and maintenance.

## Create A Pack

Clone this repo next to where the new pack folder should be created:

```bash
git clone https://github.com/h2-modpack/ModpackBootstrap.git
python ModpackBootstrap/new_pack.py \
  --pack-id speedrun \
  --pack-name "Speedrun" \
  --coordinator-package Speedrun_Modpack \
  --team adamantSpeedrun \
  --org h2pack-speedrun
```

The script prints the exact GitHub repos, Thunderstore package names, local
folders, and side effects before it creates anything. It asks for confirmation
twice because it creates repositories, pushes initial commits, and wires
submodules.

After creation:

```bash
cd speedrun-modpack
python ModpackTools/local_deploy/deploy_all.py --overwrite
```

## Naming

- `--pack-id`: internal Framework pack id, lowercase with optional hyphens.
- `--pack-name`: in-game display name.
- `--coordinator-package`: coordinator Thunderstore package suffix.
- `--team`: Thunderstore team/namespace for pack-owned packages.
- `--org`: GitHub org where the shell and coordinator repos are created.

Given `--team adamantSpeedrun` and
`--coordinator-package Speedrun_Modpack`, the coordinator package/repo is
`adamantSpeedrun-Speedrun_Modpack`.

## Validation

```bash
python -m py_compile new_pack.py bootstrap_common.py
python tests/test_bootstrap_contracts.py
```
