import os
import hybrid
import xbmc
import xbmcgui
import xbmcaddon

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
addonversion = addon.getAddonInfo('version')
addonpath = hybrid.string_decode_utf8(addon.getAddonInfo('path'))
addonstorageuser = os.path.join(hybrid.string_decode_utf8(hybrid.xbmc_translate_path('special://profile/addon_data/')), addonid)
addonstoragecache = os.path.join(addonstorageuser, 'cache')
kodiversion = xbmc.getInfoLabel('System.BuildVersion').split(' ')[0].split('-')[0]

#Busy variables
busy_main = False

#Window variables
guiMain = None
windowHome = xbmcgui.Window(10000)
