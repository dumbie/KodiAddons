import os
import sys
from datetime import datetime, timedelta
import hybrid
import player
import xbmc
import xbmcaddon
import xbmcgui

#Action variables
ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_BACKSPACE = 92
REMOTE_0 = 58
REMOTE_1 = 59
REMOTE_2 = 60
REMOTE_3 = 61
REMOTE_4 = 62
REMOTE_5 = 63
REMOTE_6 = 64
REMOTE_7 = 65
REMOTE_8 = 66
REMOTE_9 = 67
ACTION_JUMP_SMS2 = 142
ACTION_JUMP_SMS3 = 143
ACTION_JUMP_SMS4 = 144
ACTION_JUMP_SMS5 = 145
ACTION_JUMP_SMS6 = 146
ACTION_JUMP_SMS7 = 147
ACTION_JUMP_SMS8 = 148
ACTION_JUMP_SMS9 = 149

#Add-on variables
addon = xbmcaddon.Addon()
addonmonitor = xbmc.Monitor()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
addonicon = addon.getAddonInfo('icon')
addonversion = addon.getAddonInfo('version')
addonpath = hybrid.string_decode_utf8(addon.getAddonInfo('path'))
addonstorage = os.path.join(hybrid.string_decode_utf8(xbmc.translatePath('special://profile/addon_data/')), addonid)
kodiversion = xbmc.getInfoLabel('System.BuildVersion').split(' ')[0].split('-')[0]
pythonversion = sys.version_info[0]

#Busy variables
busy_main = False
busy_television = False
busy_recordings = False

#Window variables
guiMain = None
guiTelevision = None
guiRecordings = None
windowHome = xbmcgui.Window(10000)

#Thread variables
thread_refresh_epgtv = None
thread_zap_wait_timer = None

#Player variables
CustomPlayer = player.Player()
PlayerTunerCheck = datetime(1970,1,1)

#Television variables
currentBouquet = None

#Zap variables
ZapControlId = 0
ZapNumber = ''
ZapTimerForce = False
ZapDelayDateTime = datetime(1970,1,1)
