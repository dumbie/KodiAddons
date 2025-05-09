import xbmc
import xbmcaddon
import xbmcgui
import hybrid
import os

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
windowHome = xbmcgui.Window(10000)

#History variables
HistoryJson = []