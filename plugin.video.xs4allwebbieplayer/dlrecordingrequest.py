import json
import xbmcgui
import apilogin
import dlfunc
import dlrecordingevent
import dlrecordingprofile
import dlrecordingseries
import func
import metadatainfo
import path
import var

def series_add(channelId, seriesId):
    try:
        #Check channel identifier
        if func.string_isnullorempty(channelId) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt, onbekende zender.', notificationIcon, 2500, False)
            return False

        #Check record identifier
        if func.string_isnullorempty(seriesId) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt, geen of onbekende serie.', notificationIcon, 2500, False)
            return False

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen planning mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataSend = json.dumps({"channelId":channelId,"seriesId":seriesId,"isAutoDeletionEnabled":True,"episodeScope":"ALL","isChannelBoundEnabled":True}).encode('ascii')
        DownloadDataJson = dlfunc.download_gzip_json(path.recording_series_add_remove(), DownloadDataSend)

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
        dlrecordingseries.download(True)
        dlrecordingevent.download(True)
        dlrecordingprofile.download(True)

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

def series_remove(seriesId, keepRecordings=True):
    try:
        #Check record identifier
        if func.string_isnullorempty(seriesId) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt, geen of onbekende serie.', notificationIcon, 2500, False)
            return False

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataSend = json.dumps({"seriesIds":[int(seriesId)],"isKeepRecordingsEnabled":keepRecordings}).encode('ascii')
        DownloadDataJson = dlfunc.download_gzip_json(path.recording_series_add_remove(), DownloadDataSend, 'DELETE')

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
        dlrecordingseries.download(True)
        dlrecordingevent.download(True)
        dlrecordingprofile.download(True)

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

def event_add(programId):
    try:
        #Check record identifier
        if func.string_isnullorempty(programId) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt, onbekende programma.', notificationIcon, 2500, False)
            return False

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return ''

        #Download json data
        DownloadDataSend = json.dumps({"externalContentId":programId,"isAutoDeletionEnabled":True}).encode('ascii')
        DownloadDataJson = dlfunc.download_gzip_json(path.recording_event_add_remove(), DownloadDataSend)

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
        dlrecordingevent.download(True)
        dlrecordingprofile.download(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

        return metadatainfo.contentId_from_json_metadata(DownloadDataJson['resultObj']['containers'][0])
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname planning mislukt.', notificationIcon, 2500, False)
        return ''

def event_remove(recordEventId, startDeltaTime=0):
    try:
        #Check record identifier
        if func.string_isnullorempty(recordEventId) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt, onbekende programma.', notificationIcon, 2500, False)
            return False

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataSend = json.dumps([{"recordId":int(recordEventId),"startDeltaTime":int(startDeltaTime)}]).encode('ascii')
        DownloadDataJson = dlfunc.download_gzip_json(path.recording_event_add_remove(), DownloadDataSend, 'DELETE')

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
        dlrecordingevent.download(True)
        dlrecordingprofile.download(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/record.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname annulering mislukt.', notificationIcon, 2500, False)
        return False
