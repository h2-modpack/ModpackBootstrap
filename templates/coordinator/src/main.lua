-- =============================================================================
-- {{COORD_ID}}: Modpack Coordinator
-- =============================================================================
-- luacheck: globals Framework
-- Thin coordinator: wires globals, owns config/setup, delegates everything
-- else to adamant-ModpackFramework.

local mods = rom.mods
mods['SGG_Modding-ENVY'].auto()

---@diagnostic disable: lowercase-global
rom = rom
_PLUGIN = _PLUGIN
game = rom.game
modutil = mods['SGG_Modding-ModUtil']
local chalk  = mods['SGG_Modding-Chalk']
local reload = mods['SGG_Modding-ReLoad']
---@module "adamant-ModpackFramework"
---@type AdamantModpackFramework
Framework = mods["adamant-ModpackFramework"]
assert(Framework, "{{COORD_ID}}: adamant-ModpackFramework is not loaded")

local config = chalk.auto('config.lua')

local PACK_ID = "{{PACK_ID}}"
local PACK_DISPLAY_NAME = "{{PACK_DISPLAY_NAME}}"
local DEFAULT_PROFILES = {}
local FRAMEWORK_OPTS = {
    moduleOrder = {
    },
}
local frameworkInitialized = false
local frameworkCreationFailed = false
local rebuildInProgress = false

local function ensureFrameworkPack()
    if frameworkInitialized then
        return true
    end
    if frameworkCreationFailed then
        return false
    end

    local ok = Framework.createPack(PACK_ID, config, #config.Profiles, DEFAULT_PROFILES, FRAMEWORK_OPTS)
    frameworkInitialized = ok == true
    frameworkCreationFailed = not frameworkInitialized
    return frameworkInitialized
end

local function rebuildFramework()
    if rebuildInProgress or not frameworkInitialized then
        return false
    end

    rebuildInProgress = true
    frameworkInitialized = false
    frameworkCreationFailed = false
    local ok = ensureFrameworkPack()
    rebuildInProgress = false

    if not ok then
        return false
    end

    return true
end

mods.on_all_mods_loaded(function()
    Framework.registerCoordinator(PACK_ID, PACK_DISPLAY_NAME, config, rebuildFramework)
end)

local function init()
    frameworkInitialized = false
    frameworkCreationFailed = false
end

local loader = reload.auto_single()

local function registerGui()
    local callbacks = Framework.createGuiCallbacks(PACK_ID)
    rom.gui.add_imgui(callbacks.render)
    rom.gui.add_always_draw_imgui(function()
        -- Assemble on the first frame after game-load callbacks have run, so
        -- Framework discovery sees all coordinated modules without relying on
        -- dependency-pin callback ordering.
        ensureFrameworkPack()
        callbacks.alwaysDraw()
    end)
    rom.gui.add_to_menu_bar(callbacks.menuBar)
end

modutil.once_loaded.game(function()
    loader.load(registerGui, init)
end)
