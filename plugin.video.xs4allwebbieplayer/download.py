import json
from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import apilogin
import classes
import files
import func
import hybrid
import path
import var

def download_channels_radio(forceUpdate=False):
    #Check if data is already cached
    if var.ChannelsDataJsonRadio != [] and forceUpdate == False:
        return None

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent')
        }

        DownloadRequest = hybrid.urllib_request(path.channels_list_radio(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        var.ChannelsDataJsonRadio = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Radio download mislukt.', notificationIcon, 2500, False)
        return False

def download_channels_tv(forceUpdate=False):
    #Check if data is already cached
    if var.ChannelsDataJsonTelevision != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.channels_list_tv(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/television.png')
                xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.ChannelsDataJsonTelevision = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt.', notificationIcon, 2500, False)
        return False

def download_recording_event(forceUpdate=False):
    #Check if data is already cached
    if var.ChannelsDataJsonRecordingEvent != [] and forceUpdate == False:
        return None

    #Check if user has pvr access
    if var.RecordingAccess == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.recording_event(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.ChannelsDataJsonRecordingEvent = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt.', notificationIcon, 2500, False)
        return False

def download_recording_series(forceUpdate=False):
    #Check if data is already cached
    if var.ChannelsDataJsonRecordingSeries != [] and forceUpdate == False:
        return None

    #Check if user has pvr access
    if var.RecordingAccess == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.recording_series(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.ChannelsDataJsonRecordingSeries = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_yesterday(forceUpdate=False):
    #Check if data is already cached
    if var.YesterdaySearchDataJson != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.vod_yesterday(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
                xbmcgui.Dialog().notification(var.addonname, 'Gister gemist download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.YesterdaySearchLastUpdate = datetime.now()
        var.YesterdaySearchDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
        xbmcgui.Dialog().notification(var.addonname, 'Gister gemist download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_movies(forceUpdate=False):
    #Check if data is already cached
    if var.ChannelsDataJsonMovies != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.vod_movies(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
                xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.ChannelsDataJsonMovies = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
        xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_series(forceUpdate=False):
    #Check if data is already cached
    if var.ChannelsDataJsonSeries != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.vod_series(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.ChannelsDataJsonSeries = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_series_kids(forceUpdate=False):
    #Check if data is already cached
    if var.ChannelsDataJsonSeriesKids != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.vod_series_kids(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
                xbmcgui.Dialog().notification(var.addonname, 'Kids series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.ChannelsDataJsonSeriesKids = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
        xbmcgui.Dialog().notification(var.addonname, 'Kids series download mislukt.', notificationIcon, 2500, False)
        return False

def download_series_season(parentId):
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.vod_series_season(parentId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return None

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie download mislukt.', notificationIcon, 2500, False)
        return None

def download_search_program(programName):
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        programName = hybrid.urllib_quote(programName)
        DownloadRequest = hybrid.urllib_request(path.search_program(programName), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/search.png')
                xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return None

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/search.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt.', notificationIcon, 2500, False)
        return None

def download_search_kids(forceUpdate=False):
    #Check if data is already cached
    if var.KidsSearchDataJson != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.search_kids(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
                xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.KidsSearchDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
        xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt.', notificationIcon, 2500, False)
        return False

def download_search_sport(forceUpdate=False):
    #Check if data is already cached
    if var.SportSearchDataJson != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.search_sport(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
                xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.SportSearchDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
        xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt.', notificationIcon, 2500, False)
        return False

def download_search_movies(forceUpdate=False):
    #Check if data is already cached
    if var.MovieSearchDataJson != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.search_movies(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
                xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.MovieSearchDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
        xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt.', notificationIcon, 2500, False)
        return False

def download_search_series(forceUpdate=False):
    #Check if data is already cached
    if var.SeriesSearchDataJson != [] and forceUpdate == False:
        return None

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.search_series(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.SeriesSearchDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt.', notificationIcon, 2500, False)
        return False

def record_series_add(ChannelId, liveSeriesId):
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Content-Type": "application/json",
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadData = json.dumps({"channelId":ChannelId,"seriesId":liveSeriesId,"isAutoDeletionEnabled":True,"episodeScope":"ALL","isChannelBoundEnabled":True}).encode('ascii')
        DownloadRequest = hybrid.urllib_request(path.recording_series_add_remove(), data=DownloadData, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen wordt opgenomen.', notificationIcon, 2500, False)

        #Download the recording series
        download_recording_series(True)

        #Download the recording event
        download_recording_event(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_event()
            var.guiMain.count_recording_event()
            var.guiMain.count_recording_series()

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt.', notificationIcon, 2500, False)
        return False

def record_series_remove(SeriesId):
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Content-Type": "application/json",
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadData = json.dumps({"seriesIds":[SeriesId],"isKeepRecordingEnabled":True}).encode('ascii')
        DownloadRequest = hybrid.urllib_request(path.recording_series_add_remove(), data=DownloadData, headers=DownloadHeaders)
        DownloadRequest.get_method = lambda: 'DELETE'
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen opname is geannuleerd.', notificationIcon, 2500, False)

        #Download the recording series
        download_recording_series(True)

        #Download the recording event
        download_recording_event(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_event()
            var.guiMain.count_recording_event()
            var.guiMain.count_recording_series()

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt.', notificationIcon, 2500, False)
        return False

def record_program_add(ProgramId):
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Content-Type": "application/json",
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadData = json.dumps({"externalContentId":ProgramId,"isAutoDeletionEnabled":True}).encode('ascii')
        DownloadRequest = hybrid.urllib_request(path.recording_event_add_remove(), data=DownloadData, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return ''

        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma wordt opgenomen.', notificationIcon, 2500, False)

        #Download the recording event
        download_recording_event(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_event()
            var.guiMain.count_recording_event()

        return str(DownloadDataJson['resultObj']['containers'][0]['metadata']['contentId'])
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt.', notificationIcon, 2500, False)
        return ''

def record_program_remove(RecordId, StartDeltaTime=0):
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Content-Type": "application/json",
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadData = json.dumps([{"recordId":int(RecordId),"startDeltaTime":int(StartDeltaTime)}]).encode('ascii')
        DownloadRequest = hybrid.urllib_request(path.recording_event_add_remove(), data=DownloadData, headers=DownloadHeaders)
        DownloadRequest.get_method = lambda: 'DELETE'
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname is geannuleerd of verwijderd.', notificationIcon, 2500, False)

        #Download the recording event
        download_recording_event(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_event()
            var.guiMain.count_recording_event()

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt.', notificationIcon, 2500, False)
        return False

def download_epg_day(dateStringDay, forceUpdate=False):
    #Check if data is already cached
    epgDayCache = None
    for epgCache in var.EpgCacheArray:
        try:
            if epgCache.dateStringDay == dateStringDay:
                epgDayCache = epgCache
                break
        except:
            continue

    #Check if update is needed
    if epgDayCache != None:
        if forceUpdate == True:
            var.EpgCacheArray.remove(epgDayCache)
        else:
            return epgDayCache.epgJson

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken,
            'Content-Type': 'application/json'
        }

        #Download epg information
        DownloadRequest = hybrid.urllib_request(path.epg_day(dateStringDay), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn = False
                notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
                xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return None

        #Update epg information
        classAdd = classes.Class_EpgCache()
        classAdd.dateStringDay = dateStringDay
        classAdd.epgJson = DownloadDataJson
        var.EpgCacheArray.append(classAdd)

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
        xbmcgui.Dialog().notification(var.addonname, 'TV Gids laden mislukt.', notificationIcon, 2500, False)
        return None
