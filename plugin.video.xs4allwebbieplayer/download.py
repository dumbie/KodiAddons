import gzip
import json
import xbmcgui
import apilogin
import classes
import getset
import hybrid
import metadatainfo
import path
import var

def request_download_gzip(urlPath, sendData=None, sendMethod=None):
    try:
        downloadHeaders = {
            "User-Agent": getset.setting_get('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip'
        }

        #Create request
        downloadRequest = hybrid.urllib_request(urlPath, headers=downloadHeaders, data=sendData)
        if sendMethod != None:
            downloadRequest.get_method = lambda: sendMethod

        #Download information
        downloadDataHttp = hybrid.urllib_urlopen(downloadRequest)
        downloadDataInfo = downloadDataHttp.info()
        downloadDataEncoding = str(downloadDataInfo.get('Content-Encoding'))

        #Decode information
        if 'gzip' in downloadDataEncoding:
            gzipObject = hybrid.stringio_from_bytes(downloadDataHttp.read())
            gzipRead = gzip.GzipFile(fileobj=gzipObject)
            return json.load(gzipRead)
        else:
            return json.load(downloadDataHttp)
    except:
        return []

def download_channels_radio(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.RadioChannelsDataJson != [] and forceUpdate == False:
            return True

        #Download json data
        DownloadDataJson = request_download_gzip(path.channels_list_radio())

        #Check if connection is successful
        if DownloadDataJson == []:
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Radio download mislukt.', notificationIcon, 2500, False)
            return False

        var.RadioChannelsDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Radio download mislukt.', notificationIcon, 2500, False)
        return False

def download_channels_tv(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.TelevisionChannelsDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.channels_list_tv())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/television.png')
                xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.TelevisionChannelsDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Televisie download mislukt.', notificationIcon, 2500, False)
        return False

def download_recording_profile(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.RecordingProfileLoaded() == True and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname profiel download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.recording_profile())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opname profiel download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update recording variables
        var.RecordingProfileLoaded(True)
        var.RecordingAccess(metadatainfo.recording_access(DownloadDataJson))
        var.RecordingAvailableSpace(metadatainfo.recording_space(DownloadDataJson))
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname profiel download mislukt.', notificationIcon, 2500, False)
        return False

def download_recording_event(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.RecordingEventDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.recording_event())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.RecordingEventDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opnames download mislukt.', notificationIcon, 2500, False)
        return False

def download_recording_series(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.RecordingSeriesDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.recording_series())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.RecordingSeriesDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie opnames download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_day(dayDateTime, forceUpdate=False):
    try:
        #Check if data is already cached
        if var.VodDayDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
            xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.vod_day(dayDateTime))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
                xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.VodDayDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma gemist download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_movies(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.MoviesVodDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
            xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.vod_movies())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
                xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.MoviesVodDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
        xbmcgui.Dialog().notification(var.addonname, 'Films download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_series(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.SeriesVodDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.vod_series())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.SeriesVodDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Series download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_kids(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.KidsVodDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, 'Kids series download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.vod_kids())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
                xbmcgui.Dialog().notification(var.addonname, 'Kids series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.KidsVodDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
        xbmcgui.Dialog().notification(var.addonname, 'Kids series download mislukt.', notificationIcon, 2500, False)
        return False

def download_vod_series_season(parentId):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return None

        #Download json data
        DownloadDataJson = request_download_gzip(path.vod_series_season(parentId))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return None

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie download mislukt.', notificationIcon, 2500, False)
        return None

def download_search_program(programName, forceUpdate=False):
    try:
        #Check if data is already cached
        if var.SearchProgramDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/search.png')
            xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.search_program(programName))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/search.png')
                xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.SearchProgramDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/search.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt.', notificationIcon, 2500, False)
        return False

def download_search_kids(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.KidsProgramDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.search_kids())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
                xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.KidsProgramDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
        xbmcgui.Dialog().notification(var.addonname, 'Kids download mislukt.', notificationIcon, 2500, False)
        return False

def download_search_sport(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.SportProgramDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
            xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.search_sport())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
                xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.SportProgramDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/sport.png')
        xbmcgui.Dialog().notification(var.addonname, 'Sport download mislukt.', notificationIcon, 2500, False)
        return False

def download_search_movies(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.MoviesProgramDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
            xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.search_movies())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
                xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.MoviesProgramDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
        xbmcgui.Dialog().notification(var.addonname, 'Week films download mislukt.', notificationIcon, 2500, False)
        return False

def download_search_series(forceUpdate=False):
    try:
        #Check if data is already cached
        if var.SeriesProgramDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = request_download_gzip(path.search_series())

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/series.png')
                xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        var.SeriesProgramDataJson = DownloadDataJson
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/series.png')
        xbmcgui.Dialog().notification(var.addonname, 'Week series download mislukt.', notificationIcon, 2500, False)
        return False

def record_series_add(ChannelId, liveSeriesId):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataSend = json.dumps({"channelId":ChannelId,"seriesId":liveSeriesId,"isAutoDeletionEnabled":True,"episodeScope":"ALL","isChannelBoundEnabled":True}).encode('ascii')
        DownloadDataJson = request_download_gzip(path.recording_series_add_remove(), DownloadDataSend)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen wordt opgenomen.', notificationIcon, 2500, False)

        #Update recording information
        download_recording_series(True)
        download_recording_event(True)
        download_recording_profile(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()
            var.guiMain.count_recording_series()

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt.', notificationIcon, 2500, False)
        return False

def record_series_remove(SeriesId, KeepRecordings=True):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataSend = json.dumps({"seriesIds":[int(SeriesId)],"isKeepRecordingsEnabled":KeepRecordings}).encode('ascii')
        DownloadDataJson = request_download_gzip(path.recording_series_add_remove(), DownloadDataSend, 'DELETE')

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen opname is geannuleerd.', notificationIcon, 2500, False)

        #Update recording information
        download_recording_series(True)
        download_recording_event(True)
        download_recording_profile(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()
            var.guiMain.count_recording_series()

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt.', notificationIcon, 2500, False)
        return False

def record_event_add(ProgramId):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return ''

        #Download json data
        DownloadDataSend = json.dumps({"externalContentId":ProgramId,"isAutoDeletionEnabled":True}).encode('ascii')
        DownloadDataJson = request_download_gzip(path.recording_event_add_remove(), DownloadDataSend)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return ''

        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma wordt opgenomen.', notificationIcon, 2500, False)

        #Update recording information
        download_recording_event(True)
        download_recording_profile(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

        return metadatainfo.contentId_from_json_metadata(DownloadDataJson['resultObj']['containers'][0])
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt.', notificationIcon, 2500, False)
        return ''

def record_event_remove(RecordId, StartDeltaTime=0):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataSend = json.dumps([{"recordId":int(RecordId),"startDeltaTime":int(StartDeltaTime)}]).encode('ascii')
        DownloadDataJson = request_download_gzip(path.recording_event_add_remove(), DownloadDataSend, 'DELETE')

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/record.png')
                xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname is geannuleerd of verwijderd.', notificationIcon, 2500, False)

        #Update recording information
        download_recording_event(True)
        download_recording_profile(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt.', notificationIcon, 2500, False)
        return False

def download_epg_day(dayDateTime, forceUpdate=False):
    try:
        #Check if data is already cached
        epgDayCache = None
        dayDateString = dayDateTime.strftime('%Y-%m-%d')
        for epgCache in var.EpgCacheArrayDataJson:
            try:
                if epgCache.dayDateString == dayDateString:
                    epgDayCache = epgCache
                    break
            except:
                continue

        #Check if update is needed
        if epgDayCache != None:
            if forceUpdate == True:
                var.EpgCacheArrayDataJson.remove(epgDayCache)
            else:
                return epgDayCache.epgJson

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
            xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return None

        #Download json data
        DownloadDataJson = request_download_gzip(path.epg_day(dayDateTime))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
                xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return None

        #Update epg information
        classAdd = classes.Class_EpgCache()
        classAdd.dayDateString = dayDateString
        classAdd.epgJson = DownloadDataJson
        var.EpgCacheArrayDataJson.append(classAdd)

        return DownloadDataJson
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
        xbmcgui.Dialog().notification(var.addonname, 'TV Gids download mislukt.', notificationIcon, 2500, False)
        return None
