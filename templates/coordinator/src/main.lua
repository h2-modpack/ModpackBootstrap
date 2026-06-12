-- =============================================================================
-- {{COORD_ID}}: Modpack Coordinator
-- =============================================================================
-- luacheck: globals Modpack
-- Thin coordinator: wires globals, owns config/setup, delegates everything
-- else to adamant-ModpackLib.modpack.

local mods = rom.mods
mods['SGG_Modding-ENVY'].auto()

---@diagnostic disable: lowercase-global
rom = rom
_PLUGIN = _PLUGIN
game = rom.game
modutil = mods['SGG_Modding-ModUtil']
local chalk  = mods['SGG_Modding-Chalk']
local reload = mods['SGG_Modding-ReLoad']
local lib = mods["adamant-ModpackLib"]
assert(lib and type(lib.modpack) == "table", "{{COORD_ID}}: adamant-ModpackLib.modpack is not loaded")
Modpack = lib.modpack

local config = chalk.auto('config.lua')

local PACK_ID = "{{PACK_ID}}"
local PACK_DISPLAY_NAME = "{{PACK_DISPLAY_NAME}}"
local DEFAULT_PROFILES = {}
local MODPACK_OPTS = {
    moduleOrder = {
    },
}
local modpackInitialized = false
local modpackCreationFailed = false
local rebuildInProgress = false

local function ensureModpack()
    if modpackInitialized then
        return true
    end
    if modpackCreationFailed then
        return false
    end

    local ok = Modpack.createPack(PACK_ID, config, #config.Profiles, DEFAULT_PROFILES, MODPACK_OPTS)
    modpackInitialized = ok == true
    modpackCreationFailed = not modpackInitialized
    return modpackInitialized
end

local function rebuildModpack()
    if rebuildInProgress or not modpackInitialized then
        return false
    end

    rebuildInProgress = true
    modpackInitialized = false
    modpackCreationFailed = false
    local ok = ensureModpack()
    rebuildInProgress = false

    if not ok then
        return false
    end

    return true
end

mods.on_all_mods_loaded(function()
    Modpack.registerCoordinator(PACK_ID, PACK_DISPLAY_NAME, config, rebuildModpack)
end)

local function init()
    modpackInitialized = false
    modpackCreationFailed = false
end

local loader = reload.auto_single()

local function registerGui()
    local callbacks = Modpack.createGuiCallbacks(PACK_ID)
    rom.gui.add_imgui(callbacks.render)
    rom.gui.add_always_draw_imgui(function()
        -- Assemble on the first frame after game-load callbacks have run, so
        -- Modpack discovery sees all coordinated modules without relying on
        -- dependency-pin callback ordering.
        ensureModpack()
        callbacks.alwaysDraw()
    end)
    rom.gui.add_to_menu_bar(callbacks.menuBar)
end

modutil.once_loaded.game(function()
    loader.load(registerGui, init)
end)
