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
    release_all = (ROOT_DIR / "templates" / "shell" / ".github" / "workflows" / "release-all.yaml").read_text(
        encoding="utf-8"
    )

    assert "https://github.com/h2-modpack/ModpackTools.git" in new_pack_source
    assert '"ModpackTools"' in new_pack_source
    assert "ModpackTools/local_deploy/deploy_all.py" in shell_readme
    assert "ModpackTools/github/release_all.py" in release_all
    assert "ModpackTools/validate_platform_versions.py" in release_all
    assert "Setup/github/release_all.py" not in release_all
    assert "Setup/deploy/deploy_all.py" not in shell_readme


def test_coordinator_template_uses_current_framework_contract() -> None:
    main_lua = (ROOT_DIR / "templates" / "coordinator" / "src" / "main.lua").read_text(encoding="utf-8")

    assert "Framework.createPack" in main_lua
    assert "Framework.createGuiCallbacks" in main_lua
    assert "rom.gui.add_imgui(callbacks.render)" in main_lua
    assert "rom.gui.add_always_draw_imgui(callbacks.alwaysDraw)" in main_lua
    assert "rom.gui.add_to_menu_bar(callbacks.menuBar)" in main_lua
    assert "Framework.tryInit" not in main_lua


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
        test_coordinator_template_uses_current_framework_contract,
        test_coordinator_template_owns_generated_assets,
    ]

    for test in tests:
        test()
    print(f"{len(tests)} bootstrap contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
