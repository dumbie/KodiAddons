import os
import xbmcaddon
import xbmcgui
import hybrid

#Action variables
ACTION_PREVIOUS_MENU = 10
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_BACKSPACE = 92

#Add-on variables
addon = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
addonicon = addon.getAddonInfo('icon')
addonpath = hybrid.string_decode_utf8(addon.getAddonInfo('path'))
addonstorage = os.path.join(hybrid.string_decode_utf8(hybrid.xbmc_translate_path('special://profile/addon_data/')), addonid)

#Busy variables
busy_main = False

#Window variables
guiMain = None
windowHome = xbmcgui.Window(10000)
