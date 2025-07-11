from datetime import datetime, timedelta
import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import getset
import hybrid
import monitorclass
import threadclass

#Action variables
ACTION_NONE = 0
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10
ACTION_SHOW_INFO = 11
ACTION_PAUSE = 12
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_STEP_FORWARD = 20
ACTION_STEP_BACK = 21
ACTION_SHOW_OSD = 24
ACTION_PLAYER_FORWARD = 77
ACTION_PLAYER_REWIND = 78
ACTION_PLAYER_PLAY = 79
ACTION_SEARCH_FUNCTION = 122
ACTION_PLAYER_PLAYPAUSE = 229
ACTION_DELETE_ITEM = 80
ACTION_VOLUME_UP = 88
ACTION_VOLUME_DOWN = 89
ACTION_MUTE = 91
ACTION_BACKSPACE = 92
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_RIGHT_CLICK = 101
ACTION_MOUSE_MOVE = 107
ACTION_CONTEXT_MENU = 117
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
ACTION_TELETEXT_RED = 215
ACTION_TELETEXT_GREEN = 216
ACTION_TELETEXT_YELLOW = 217
ACTION_TELETEXT_BLUE = 218

#Window variables
guiMain = None
guiPlayer = None
guiAlarm = None
guiDialog = None
guiTelevision = None
guiRecorded = None
guiRecordingEvent = None
guiRecordingSeries = None
guiVod = None
guiKids = None
guiSearch = None
guiMovies = None
guiSport = None
guiSeries = None
guiSeriesSeason = None
guiRadio = None
guiStb = None
guiEpg = None
guiHelp = None
guiHidden = None
guiWelcome = None
windowHome = xbmcgui.Window(10000)
WINDOW_HOME = 10000
WINDOW_DIALOG_PLAYER_PROCESS_INFO = 10116
WINDOW_DIALOG_VIDEO_OSD_SETTINGS = 10123
WINDOW_DIALOG_AUDIO_OSD_SETTINGS = 10124
WINDOW_DIALOG_SUBTITLE_OSD_SETTINGS = 10159
WINDOW_FULLSCREEN_VIDEO = 12005
WINDOW_VISUALISATION = 12006
WINDOW_ADDON = 13000

#Add-on variables
addon = xbmcaddon.Addon()
addonmonitor = monitorclass.Class_MonitorCustom()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
addonicon = addon.getAddonInfo('icon')
addonversion = addon.getAddonInfo('version')
addonpath = hybrid.string_decode_utf8(addon.getAddonInfo('path'))
addonstorageuser = os.path.join(hybrid.string_decode_utf8(hybrid.xbmc_translate_path('special://profile/addon_data/')), addonid)
addonstoragecache = os.path.join(addonstorageuser, 'cache')
kodiversion = xbmc.getInfoLabel('System.BuildVersion').split(' ')[0].split('-')[0]

#Launch variables
LaunchUrl = ''
LaunchHandle = 0
LaunchArgument = ''

#Dialog variables
DialogResult = None

#Cache variables
CacheCleanTimeChannels = 240 * 60 #4h
CacheCleanTimeEpg = 120 * 60 #2h
def CacheCleanTimeOther():
     return int(getset.setting_get('CacheCleanTimeOther')) * 60

#Thread variables
thread_notification = threadclass.Class_ThreadSafe()
thread_check_requirements = threadclass.Class_ThreadSafe()
thread_zap_wait_timer = threadclass.Class_ThreadSafe()
thread_update_television_program = threadclass.Class_ThreadSafe()
thread_update_epg_program = threadclass.Class_ThreadSafe()
thread_update_epg_channel = threadclass.Class_ThreadSafe()
thread_update_playergui_info = threadclass.Class_ThreadSafe()
thread_hide_playergui_info = threadclass.Class_ThreadSafe()
thread_sleep_timer = threadclass.Class_ThreadSafe()

#Api variables
def ApiLoginFailCount(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, 0)
    else:
         return getset.global_pickle_set(varName, setObject)

def ApiEndpointUrl(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, '')
    else:
         return getset.global_pickle_set(varName, setObject)

def ApiLoggedIn(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, False)
    else:
         return getset.global_pickle_set(varName, setObject)

def ApiHomeAccess(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, True)
    else:
         return getset.global_pickle_set(varName, setObject)

def ApiLoginLastUsername(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, '')
    else:
         return getset.global_pickle_set(varName, setObject)

def ApiLoginLastDateTime(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, datetime(1970,1,1))
    else:
         return getset.global_pickle_set(varName, setObject)

def ApiLoginCookie(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, '')
    else:
         return getset.global_pickle_set(varName, setObject)

#Favorite variables
FavoriteTelevisionJson = []
FavoriteRadioJson = []

#Hidden variables
HiddenChannelMode = ''
HiddenChannelChanged = False
HiddenTelevisionJson = []
HiddenRadioJson = []

#Search variables
SearchSelectIdentifier = ''
SearchTermResult = ''
SearchProgramDataJson = []

#Kids variables
KidsProgramSelectIdentifier = ''
KidsEpisodeSelectIdentifier = ''
KidsProgramDataJson = []
KidsVodDataJson = []

#Sport variables
SportSelectIdentifier = ''
SportProgramDataJson = []

#Television variables
TelevisionChannelIdsPlayableArray = []
TelevisionChannelIdsPlayableString = ''

#Channel variables
StbChannelsDataJson = []
WebChannelsDataJson = []

#Vod variables
VodSelectIdentifier = ''
VodDayLoadDateTime = datetime.now()
VodDayOffsetPast = 10

#Movies variables
MovieSelectIdentifier = ''
MoviesProgramDataJson = []
MoviesVodDataJson = []

#Series variables
SeriesProgramSelectIdentifier = ''
SeriesEpisodeSelectIdentifier = ''
SeriesProgramDataJson = []
SeriesVodDataJson = []

#Recording variables
RecordedSelectIdentifier = ''
RecordingProcessMinutes = 10
RecordingEventDataJson = []
RecordingSeriesDataJson = []
def RecordingProfileLoaded(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, False)
    else:
         return getset.global_pickle_set(varName, setObject)

def RecordingAccess(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, False)
    else:
         return getset.global_pickle_set(varName, setObject)

def RecordingAvailableSpace(setObject=None):
    varName = str(sys._getframe().f_code.co_name)
    if setObject == None:
         return getset.global_pickle_get(varName, "Onbekende ruimte beschikbaar")
    else:
         return getset.global_pickle_set(varName, setObject)

#Epg variables
EpgCurrentLoadDateTime = datetime.now()
EpgPreviousLoadDateTime = datetime(1970,1,1)
EpgCurrentChannelName = ''
EpgCurrentChannelId = ''
EpgPreviousChannelId = ''
EpgSelectIdentifier = ''
EpgNavigateIdentifier = ''
EpgDaysOffsetFuture = 5
EpgCacheDaysArray = []

#Program variables
ProgramRerunSearchTerm = ['loop:', 'herhaling', 'herhalingen', 'samenvatting', 'nabeschouwing', 'terugblik', 'highlights', 'hoogtepunten', 'round-up', 'replay', 'wiederholung']

#Zap variables
ZapControlId = 0
ZapNumberString = ''
ZapHintString = ''
ZapTimerForce = False
ZapDelayDateTime = datetime(1970,1,1)

#Sleep variables
SleepEndingMinutes = 9999

#Alarm variables
AlarmDataJson = []

#Welcome variables
WelcomeResult = None

#Widevine variables
WidevineUpdating = False

#Service - Alarm variables
thread_alarm_timer = threadclass.Class_ThreadSafe()

#Service - Cache variables
thread_cache_clean = threadclass.Class_ThreadSafe()

#Service - Proxy variables
ProxyServer = None
thread_proxy_server = threadclass.Class_ThreadSafe()
