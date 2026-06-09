# ModpackBootstrap

One-time bootstrapper for creating a Hades II modpack workspace.

Use this repo to create a new shell repo and coordinator repo. The generated
shell installs `ModpackTools/` as the ongoing pack toolbelt for module
scaffolding, deployment, release orchestration, and maintenance.

Start with [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for the full
new-pack walkthrough.

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

- `--pack-id`: internal Framework pack id and shell repo slug. It must use
  lowercase letters/numbers with single hyphen separators. The shell repo and
  local folder are always `{pack-id}-modpack`.
- `--pack-name`: in-game display name.
- `--coordinator-package`: coordinator Thunderstore package suffix. It must use
  letters/numbers/underscores, no leading/trailing underscore, and no repeated
  underscores.
- `--team`: Thunderstore team/namespace for pack-owned packages. It must use
  letters/numbers/underscores and cannot start or end with `_`.
- `--org`: GitHub org where the shell and coordinator repos are created. It
  must use letters/numbers with single hyphen separators.

Example mapping:

| Input | Output |
| --- | --- |
| `--pack-id speedrun` | shell repo/folder: `speedrun-modpack` |
| `--pack-name "Speedrun"` | in-game display name: `Speedrun` |
| `--team adamantSpeedrun` | Thunderstore namespace: `adamantSpeedrun` |
| `--coordinator-package Speedrun_Modpack` | coordinator package suffix: `Speedrun_Modpack` |
| team + coordinator package | coordinator package/repo/folder: `adamantSpeedrun-Speedrun_Modpack` |

## Validation

```bash
python -m py_compile new_pack.py bootstrap_common.py
python tests/test_bootstrap_contracts.py
```
