from datetime import datetime, timedelta
import download
import xbmc
import xbmcgui
import apilogin
import func
import path
import streamadjust
import streamcheck
import var

def play_tv(listItem, Windowed=False, OpenOverlay=True, ShowInformation=False, SeekOffsetSecEnd=0):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Check channel properties
        streamcheck.check_tv(listItem)

        #Get channel properties
        NewStreamAssetId = listItem.getProperty('StreamAssetId')
        NewChannelId = listItem.getProperty('ChannelId')

        #Check channel properties
        if func.string_isnullorempty(NewChannelId):
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
            return

        if func.string_isnullorempty(NewStreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Allow longer back seeking
        DateTimeUtc = datetime.utcnow() - timedelta(minutes=400)
        StartString = '&time=' + str(func.datetime_to_ticks(DateTimeUtc))

        #Download television stream url
        DownloadDataJson = download.request_download_gzip(path.stream_url_tv(NewChannelId, NewStreamAssetId) + StartString)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/television.png')
                xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
                return

        #Update channel settings and variables
        CurrentChannelId = var.addon.getSetting('CurrentChannelId')
        if CurrentChannelId != NewChannelId:
            var.addon.setSetting('LastChannelId', CurrentChannelId)
        var.addon.setSetting('CurrentChannelId', NewChannelId)
        xbmc.sleep(100)

        #Get downloaded stream url
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']

        #Update stream url with bitrate setting
        StreamUrl = streamadjust.adjust_streamurl_bitrate(StreamUrl)

        #Update stream url with localhost proxy
        StreamUrl = streamadjust.adjust_streamurl_proxy(StreamUrl)

        #Update listitem with other stream properties
        streamadjust.adjust_listitem_properties(listItem)

        #Update listitem with input stream properties
        streamadjust.adjust_listitem_inputstream(listItem, DownloadDataJson, True)

        #Start playing the media
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, OpenOverlay, ShowInformation, SeekOffsetSecEnd=SeekOffsetSecEnd)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)

def play_radio(listItem, Windowed=False):
    try:
        #Check channel properties
        streamcheck.check_radio(listItem)

        #Get channel properties
        ChannelId = listItem.getProperty('ChannelId')
        StreamUrl = listItem.getProperty('StreamUrl')

        #Check channel properties
        if func.string_isnullorempty(ChannelId):
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
            return

        #Update channel settings and variables
        var.addon.setSetting('CurrentRadioId', ChannelId)
        xbmc.sleep(100)

        #Start playing the media
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, StreamType='audio')
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)

def play_program(listItem, Windowed=False):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Get the program id
        ProgramId = listItem.getProperty('ProgramId')

        #Check program properties
        if func.string_isnullorempty(ProgramId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige programma informatie.', notificationIcon, 2500, False)
            return

        #Download program details
        DownloadDataJson = download.request_download_gzip(path.detail_program(ProgramId))

        #Check program properties
        streamcheck.check_program(listItem, DownloadDataJson)

        #Get the stream asset id
        StreamAssetId = listItem.getProperty('StreamAssetId')

        #Check the set stream asset id
        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download program stream url
        DownloadDataJson = download.request_download_gzip(path.stream_url_program(ProgramId, StreamAssetId))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
                xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
                return

        #Get the downloaded stream url
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']

        #Update stream url with bitrate setting
        StreamUrl = streamadjust.adjust_streamurl_bitrate(StreamUrl)

        #Update stream url with localhost proxy
        StreamUrl = streamadjust.adjust_streamurl_proxy(StreamUrl)

        #Update listitem with other stream properties
        streamadjust.adjust_listitem_properties(listItem)

        #Update listitem with input stream properties
        streamadjust.adjust_listitem_inputstream(listItem, DownloadDataJson)

        #Get stream start offset time
        SeekOffsetSecStart = int(var.addon.getSetting('PlayerSeekOffsetStart')) * 60

        #Start playing the media
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, SeekOffsetSecStart=SeekOffsetSecStart)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)

def play_vod(listItem, Windowed=False):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Get the program id
        ProgramId = listItem.getProperty('ProgramId')

        #Check vod properties
        if func.string_isnullorempty(ProgramId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige vod informatie.', notificationIcon, 2500, False)
            return

        #Download program userdata
        DownloadDataJson = download.request_download_gzip(path.detail_vod(ProgramId))

        #Check vod properties
        streamcheck.check_vod(listItem, DownloadDataJson)

        #Get the stream asset id
        StreamAssetId = listItem.getProperty('StreamAssetId')

        #Check the set stream asset id
        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download the program stream url
        DownloadDataJson = download.request_download_gzip(path.stream_url_vod(ProgramId, StreamAssetId))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
                xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
                return

        #Get the downloaded stream url
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']

        #Update stream url with bitrate setting
        StreamUrl = streamadjust.adjust_streamurl_bitrate(StreamUrl)

        #Update stream url with localhost proxy
        StreamUrl = streamadjust.adjust_streamurl_proxy(StreamUrl)

        #Update listitem with other stream properties
        streamadjust.adjust_listitem_properties(listItem)

        #Update listitem with input stream properties
        streamadjust.adjust_listitem_inputstream(listItem, DownloadDataJson)

        #Start playing the media
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)

def play_recorded(listItem, Windowed=False):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Check recorded properties
        streamcheck.check_recorded(listItem)

        #Get stream asset id
        StreamAssetId = listItem.getProperty('StreamAssetId')
        ProgramRecordEventId = listItem.getProperty('ProgramRecordEventId')

        #Check recorded properties
        if func.string_isnullorempty(ProgramRecordEventId):
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige opname informatie.', notificationIcon, 2500, False)
            return

        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download the program stream url
        DownloadDataJson = download.request_download_gzip(path.stream_url_recording(ProgramRecordEventId, StreamAssetId))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
                xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
                return

        #Get the downloaded stream url
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']

        #Update stream url with bitrate setting
        StreamUrl = streamadjust.adjust_streamurl_bitrate(StreamUrl)

        #Update stream url with localhost proxy
        StreamUrl = streamadjust.adjust_streamurl_proxy(StreamUrl)

        #Update listitem with other stream properties
        streamadjust.adjust_listitem_properties(listItem)

        #Update listitem with input stream properties
        streamadjust.adjust_listitem_inputstream(listItem, DownloadDataJson)

        #Get stream start offset time
        SeekOffsetSecStart = 0
        ProgramDeltaTimeStart = listItem.getProperty('ProgramDeltaTimeStart')
        if func.string_isnullorempty(ProgramDeltaTimeStart) == False and ProgramDeltaTimeStart != '0':
            SeekOffsetSecStart = func.ticks_to_seconds(ProgramDeltaTimeStart)
        if SeekOffsetSecStart == 0:
            SeekOffsetSecStart = int(var.addon.getSetting('PlayerSeekOffsetStart')) * 60

        #Start playing the media
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, SeekOffsetSecStart=SeekOffsetSecStart)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)
