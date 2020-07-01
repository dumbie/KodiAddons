import os
import var
import xbmc
import xbmcgui
import xbmcaddon

#Action variables
ACTION_PREVIOUS_MENU = 10
ACTION_BACKSPACE = 92

#Add-on variables
addon = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
addonicon = addon.getAddonInfo('icon')
addonpath = addon.getAddonInfo('path').decode('UTF-8')
addonstorage = os.path.join(xbmc.translatePath('special://profile/addon_data/').decode('UTF-8'), addonid)

#Window variables
guiMain = None
windowHome = xbmcgui.Window(10000)
