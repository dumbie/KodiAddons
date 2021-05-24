import os
from datetime import datetime, timedelta
import hybrid
import player
import var
import xbmc
import xbmcaddon
import xbmcgui

#Action variables
ACTION_NONE = 0
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10
ACTION_PAUSE = 12
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_STEP_FORWARD = 20
ACTION_STEP_BACK = 21
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

#Window variables
guiMain = None
guiPlayer = None
guiAlarm = None
guiDialog = None
guiTelevision = None
guiRecorded = None
guiRecordingEvent = None
guiRecordingSeries = None
guiYesterday = None
guiKids = None
guiSearch = None
guiMovies = None
guiSport = None
guiSeries = None
guiSeriesSeason = None
guiRadio = None
guiEpg = None
guiHelp = None
windowHome = xbmcgui.Window(10000)
WINDOW_DIALOG_VIDEO_OSD_SETTINGS = 10123
WINDOW_DIALOG_AUDIO_OSD_SETTINGS = 10124
WINDOW_FULLSCREEN_VIDEO = 12005
WINDOW_VISUALISATION = 12006
WINDOW_ADDON = 13000

#Add-on variables
addon = xbmcaddon.Addon()
addonmonitor = xbmc.Monitor()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
addonicon = addon.getAddonInfo('icon')
addonversion = addon.getAddonInfo('version')
addonpath = hybrid.string_decode_utf8(addon.getAddonInfo('path'))
addonstorage = os.path.join(hybrid.string_decode_utf8(hybrid.xbmc_translate_path('special://profile/addon_data/')), addonid)
kodiversion = xbmc.getInfoLabel('System.BuildVersion').split(' ')[0].split('-')[0]

#Launch variables
LaunchArgument = ''

#Dialog variables
DialogResult = None

#Thread variables
thread_check_requirements = None
thread_zap_wait_timer = None
thread_channel_delay_timer = None
thread_update_television_epg = None
thread_update_epg_progress = None
thread_update_playergui_info = None
thread_hide_playergui_info = None
thread_sleep_timer = None
thread_alarm_timer = None
thread_login_auto = None

#Player variables
PlayerCustom = player.PlayerCustom()
PlayerWindowed = False
PlayerOverlay = False

#Api variables
ApiLoggedIn = False
ApiHomeAccess = True
ApiLastLogin = datetime(1970, 1, 1)
ApiLoginCookie = ''
ApiLoginToken = ''
ApiLoginCount = 0

#Favorite variables
FavoriteTelevisionDataJson = []

#Search variables
SearchFilterTerm = ''
SearchDownloadSearchTerm = ''
SearchDownloadResultJson = []
SearchHistorySearchJson = []

#Kids variables
KidsSearchDataJson = []
ChannelsDataJsonSeriesKids = []

#Sport variables
SportSearchDataJson = []

#Radio variables
ChannelsDataJsonRadio = []

#Television variables
ChannelDelayDateTime = datetime(1970,1,1)
LoadChannelFavoritesOnly = False
ChannelIdsPlayable = []
ChannelsDataJsonTelevision = []

#Yesterday variables
YesterdaySearchLastUpdate = datetime(1970,1,1)
YesterdaySearchDataJson = []

#Movies variables
MovieSearchDataJson = []
ChannelsDataJsonMovies = []

#Series variables
SeriesSearchDataJson = []
ChannelsDataJsonSeries = []

#Recording variables
RecordingAccess = True
RecordingProcessMinutes = 15
ChannelsDataJsonRecordingEvent = []
ChannelsDataJsonRecordingSeries = []

#Epg variables
EpgDaysOffsetPast = 7
EpgDaysOffsetFuture = 7
EpgRerunSearchTerm = ['loop:', 'herhaling', 'herhalingen', 'samenvatting', 'nabeschouwing', 'terugblik', 'highlights', 'hoogtepunten']
EpgCacheArray = []

#Program variables
ProgramTitleStripStrings = ['B.O.Z.: ', "Telekids Mini's: ", 'Doc: ', 'Marathon: ', 'Zappbios: ', 'Film: ', 'Premiere: ', u'Premi\xe8re: ']
ProgramTitleStripRegEx = ['Detectives op (.*?): ']

#Zap variables
ZapControlId = 0
ZapNumber = ''
ZapTimerForce = False
ZapDelayDateTime = datetime(1970,1,1)

#Sleep variables
SleepEndingMinutes = 9999

#Alarm variables
AlarmDataJson = []

#Widevine variables
WidevineUpdating = False