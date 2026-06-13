from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import new_pack  # noqa: E402


def assert_raises(validator, value) -> None:
    try:
        validator(value)
    except ValueError:
        return
    raise AssertionError(f"invalid value accepted: {value!r}")


def test_new_pack_uses_explicit_coordinator_package() -> None:
    assert new_pack.coordinator_id("adamantSpeedrun", "Speedrun_Modpack") == "adamantSpeedrun-Speedrun_Modpack"
    assert new_pack.coordinator_id("adamantRunDirector", "RunDirector_Modpack") == "adamantRunDirector-RunDirector_Modpack"


def test_new_pack_validation_rejects_ambiguous_names() -> None:
    new_pack.validate_pack_id("speedrun")
    new_pack.validate_pack_id("run-director")
    new_pack.validate_single_line("Run Director", "--pack-name")
    new_pack.validate_team("adamantRunDirector")
    new_pack.validate_coordinator_package("RunDirector_Modpack")
    new_pack.validate_org("h2pack-rundirector")

    assert_raises(new_pack.validate_pack_id, "RunDirector")
    assert_raises(new_pack.validate_pack_id, "run_director")
    assert_raises(new_pack.validate_pack_id, "run--director")
    assert_raises(lambda value: new_pack.validate_single_line(value, "--pack-name"), "")
    assert_raises(lambda value: new_pack.validate_single_line(value, "--pack-name"), "Two\nLines")
    assert_raises(new_pack.validate_team, "_adamant")
    assert_raises(new_pack.validate_team, "adamant-speedrun")
    assert_raises(new_pack.validate_coordinator_package, "RunDirector-Modpack")
    assert_raises(new_pack.validate_coordinator_package, "RunDirector__Modpack")
    assert_raises(new_pack.validate_org, "-h2pack")
    assert_raises(new_pack.validate_org, "h2pack_rundirector")


def test_bootstrap_installs_modpack_tools_not_setup() -> None:
    new_pack_source = (ROOT_DIR / "new_pack.py").read_text(encoding="utf-8")
    shell_readme = (ROOT_DIR / "templates" / "shell" / "README.md").read_text(encoding="utf-8")
    shell_ci = (ROOT_DIR / "templates" / "shell" / ".github" / "workflows" / "ci.yaml").read_text(
        encoding="utf-8"
    )
    release_all = (ROOT_DIR / "templates" / "shell" / ".github" / "workflows" / "release-all.yaml").read_text(
        encoding="utf-8"
    )
    smoke = (ROOT_DIR / "templates" / "shell" / "tests" / "smoke.lua").read_text(encoding="utf-8")
    smoke_manifest_path = ROOT_DIR / "templates" / "shell" / "tests" / "smoke_manifest.lua"
    test_all_path = ROOT_DIR / "templates" / "shell" / "tests" / "test_all.lua"

    assert "https://github.com/h2-modpack/ModpackTools.git" in new_pack_source
    assert '"ModpackTools"' in new_pack_source
    assert "ModpackTools/local_deploy/deploy_all.py" in shell_readme
    assert "ModpackTools/local_test/all.py" in shell_readme
    assert "ModpackTools/local_test/all.py" in new_pack_source
    assert "ModpackTools/new_module/register_submodules.py" in shell_readme
    assert "ModpackTools/new_module/register_submodules.py" in new_pack_source
    assert "lua tests/smoke.lua" in shell_readme
    assert "lua tests/test_all.lua" not in shell_readme
    assert "lua tests/test_all.lua" not in new_pack_source
    assert "tests/smoke_manifest.lua" not in shell_readme
    assert "tests/smoke_manifest.lua" not in new_pack_source
    assert "Run smoke" in shell_ci
    assert "Run smoke manifest" not in shell_ci
    assert "lua tests/smoke.lua" in shell_ci
    assert "ModpackTools/validate_platform_versions.py" not in shell_ci
    assert "ModpackTools/run ModpackTools/test_all.py" not in shell_ci
    assert "leafo/gh-actions-lua@v10" in shell_ci
    assert "leafo/gh-actions-luarocks@v4" not in shell_ci
    assert "ModpackTools/github/release_all.py" in release_all
    assert "Validate platform dependency versions" in release_all
    assert "python3 ModpackTools/validate_platform_versions.py" in release_all
    assert 'TOOLS_REF: "release-tools-V3"' in release_all
    assert '--module-field "tools-ref=$TOOLS_REF"' in release_all
    assert '--coordinator-field "tools-ref=$TOOLS_REF"' in release_all
    assert "--verify-ci" in release_all
    assert "Verify shell CI passed for release commit" in release_all
    assert "--workflow \"ci.yaml\"" in release_all
    assert "--coordinator-repo \"{{COORD_ID}}\"" in release_all
    assert "--pin-coordinator-module-deps" in release_all
    assert "--core-repo" not in release_all
    assert "lib-version" in release_all
    assert "--dependency-repo" not in release_all
    assert "apt-get" not in release_all
    assert "lua5.2" not in release_all
    assert "luac5.2" not in release_all
    assert "Run ModpackLib tests" not in release_all
    assert "Validate module sources" not in release_all
    assert "leafo/gh-actions-lua@" not in release_all
    assert "Run ModpackFramework tests" not in release_all
    assert "adamant-ModpackFramework" not in release_all
    assert "Setup/github/release_all.py" not in release_all
    assert "Setup/deploy/deploy_all.py" not in shell_readme
    assert not smoke_manifest_path.exists()
    assert not test_all_path.exists()
    assert 'dofile("adamant-ModpackLib/tests/harness/shell_smoke.lua")' in smoke
    assert "shellSmoke.run" in smoke
    assert "rootDir = \".\"" in smoke
    assert "smokeRunner.assertManifest" not in smoke
    assert "smoke_manifest" not in smoke


def test_coordinator_template_uses_current_modpack_contract() -> None:
    main_lua = (ROOT_DIR / "templates" / "coordinator" / "src" / "main.lua").read_text(encoding="utf-8")

    assert "Modpack.createPack" in main_lua
    assert "local PACK_DISPLAY_NAME" in main_lua
    assert 'assert(lib and type(lib.modpack) == "table"' in main_lua
    assert "local function ensureModpack()" in main_lua
    assert "local modpackCreationFailed = false" in main_lua
    assert "Modpack.registerCoordinator(PACK_ID, PACK_DISPLAY_NAME, config, rebuildModpack)" in main_lua
    assert "Modpack.createPack(PACK_ID, config, #config.Profiles, DEFAULT_PROFILES, MODPACK_OPTS)" in main_lua
    assert "Modpack.createGuiCallbacks" in main_lua
    assert "rom.gui.add_imgui(callbacks.render)" in main_lua
    assert "rom.gui.add_always_draw_imgui(function()" in main_lua
    assert "ensureModpack()" in main_lua
    assert "callbacks.alwaysDraw()" in main_lua
    assert "rom.gui.add_to_menu_bar(callbacks.menuBar)" in main_lua
    assert "WINDOW_TITLE" not in main_lua
    assert "adamant-ModpackFramework" not in main_lua
    assert "Framework." not in main_lua
    assert "Framework.createPack(PACK_ID, PACK_DISPLAY_NAME" not in main_lua
    assert "FRAMEWORK_OPTS" not in main_lua
    assert "ensureFrameworkPack" not in main_lua
    assert "type(Framework.createPack)" not in main_lua
    assert "type(Framework.registerCoordinator)" not in main_lua
    assert "type(Framework.createGuiCallbacks)" not in main_lua
    assert "Framework.tryInit" not in main_lua


def test_coordinator_release_preserves_module_dependency_pins() -> None:
    release_yaml = (
        ROOT_DIR / "templates" / "coordinator" / ".github" / "workflows" / "release.yaml"
    ).read_text(encoding="utf-8")

    assert "fetch-depth: 0" in release_yaml
    assert "Checkout ModpackTools" in release_yaml
    assert "h2-modpack/ModpackTools" in release_yaml
    assert 'tools-ref:' in release_yaml
    assert 'default: "release-tools-V3"' in release_yaml
    assert "ref: ${{ inputs['tools-ref'] }}" in release_yaml
    assert "actions/checkout@v4" not in release_yaml
    assert "leafo/gh-actions-lua@v10" not in release_yaml
    assert "leafo/gh-actions-luarocks@v4" not in release_yaml
    assert "leafo/gh-actions-lua@35bcb06abec04ec87df82e08caa84d545348536e" in release_yaml
    assert "leafo/gh-actions-luarocks@e65774a6386cb4f24e293dca7fc4ff89165b64c5" in release_yaml
    assert "github/prepare_package_release.py" in release_yaml
    assert "github/check_thunderstore_release.py" in release_yaml
    assert "steps.thunderstore.outputs.published != 'true'" in release_yaml
    assert "steps.thunderstore.outputs.published == 'true'" in release_yaml
    assert "--allow-empty" in release_yaml
    assert "--release-notes-output .release-notes.md" in release_yaml
    assert 'git commit --message "chore(release): ${{ inputs.tag }}"' in release_yaml
    assert "git push --atomic origin HEAD:${{ github.ref_name }} refs/tags/${{ inputs.tag }}" in release_yaml
    assert "--notes-file '.release-notes.md'" in release_yaml
    assert "Rotate unreleased section in changelog" not in release_yaml
    assert "Rotate version in Thunderstore CLI config" not in release_yaml
    assert "Rotate module dependency versions" not in release_yaml
    assert "# -- submodules-start --" not in release_yaml


def test_coordinator_template_owns_generated_assets() -> None:
    coordinator_template = ROOT_DIR / "templates" / "coordinator"

    assert (ROOT_DIR / "LICENSE").is_file()
    assert not (ROOT_DIR / "icon.png").exists()
    assert (coordinator_template / "LICENSE").is_file()
    assert (coordinator_template / "icon.png").is_file()
    assert not (coordinator_template / "CONTRIBUTING.md").exists()


def main() -> int:
    tests = [
        test_new_pack_uses_explicit_coordinator_package,
        test_new_pack_validation_rejects_ambiguous_names,
        test_bootstrap_installs_modpack_tools_not_setup,
        test_coordinator_template_uses_current_modpack_contract,
        test_coordinator_release_preserves_module_dependency_pins,
        test_coordinator_template_owns_generated_assets,
    ]

    for test in tests:
        test()
    print(f"{len(tests)} bootstrap contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
