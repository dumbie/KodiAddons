from datetime import datetime, timedelta
import xbmcgui
import apilogin
import dlfunc
import func
import getset
import metadatainfo
import path
import player
import streamadjust
import var

def play_tv(listItem, Windowed=False, OpenOverlay=True, ShowInformation=False, SeekOffsetSecEnd=0):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

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

        #Allow longer backwards seeking
        PlayerSeekBackMinutes = int(getset.setting_get('PlayerSeekBackMinutes'))
        DateTimeUtc = datetime.utcnow() - timedelta(minutes=PlayerSeekBackMinutes)
        StartString = '&time=' + str(func.datetime_to_ticks(DateTimeUtc))

        #Download television stream url
        DownloadDataJson = dlfunc.download_gzip_json(path.stream_url_tv(NewChannelId, NewStreamAssetId) + StartString)

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
        CurrentChannelId = getset.setting_get('CurrentChannelId', True)
        if CurrentChannelId != NewChannelId:
            getset.setting_set('CurrentChannelId', NewChannelId)
            getset.setting_set('LastChannelId', CurrentChannelId)

        #Get downloaded stream url
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']

        #Update stream url with uhd workaround
        if NewChannelId == "2495":
            StreamUrl = streamadjust.adjust_workaround_uhd(StreamUrl)

        #Update stream url with bitrate setting
        StreamUrl = streamadjust.adjust_streamurl_bitrate(StreamUrl)

        #Update stream url with localhost proxy
        StreamUrl = streamadjust.adjust_streamurl_proxy(StreamUrl)

        #Update listitem with other stream properties
        streamadjust.adjust_listitem_properties(listItem)

        #Update listitem with input stream properties
        streamadjust.adjust_listitem_inputstream(listItem, DownloadDataJson, True)

        #Start playing the media
        player.PlayCustom(StreamUrl, listItem, Windowed, OpenOverlay, ShowInformation, SeekOffsetSecEnd=SeekOffsetSecEnd)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)

def play_radio(listItem, Windowed=False):
    try:
        #Get channel properties
        ChannelId = listItem.getProperty('ChannelId')
        StreamUrl = listItem.getProperty('StreamUrl')

        #Check channel properties
        if func.string_isnullorempty(ChannelId):
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
            return

        if func.string_isnullorempty(StreamUrl):
            notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige stream informatie.', notificationIcon, 2500, False)
            return

        #Update channel settings and variables
        getset.setting_set('CurrentRadioId', ChannelId)

        #Start playing the media
        player.PlayCustom(StreamUrl, listItem, Windowed)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)

def play_stb(listItem, Windowed=False):
    try:
        #Get channel properties
        ChannelId = listItem.getProperty('ChannelId')
        StreamUrl = listItem.getProperty('StreamUrl')

        #Check channel properties
        if func.string_isnullorempty(ChannelId):
            notificationIcon = path.resources('resources/skins/default/media/common/stb.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
            return

        if func.string_isnullorempty(StreamUrl):
            notificationIcon = path.resources('resources/skins/default/media/common/stb.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige stream informatie.', notificationIcon, 2500, False)
            return

        #Update channel settings and variables
        getset.setting_set('CurrentStbId', ChannelId)

        #Start playing the media
        player.PlayCustom(StreamUrl, listItem, Windowed)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/stb.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)

def play_program(listItem, Windowed=False):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Get program properties
        ProgramId = listItem.getProperty('ProgramId')

        #Check program properties
        if func.string_isnullorempty(ProgramId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige programma informatie.', notificationIcon, 2500, False)
            return

        #Download program details
        DownloadDataJson = dlfunc.download_gzip_json(path.detail_program(ProgramId))

        #Get the stream asset id
        StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(DownloadDataJson)

        #Check the set stream asset id
        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download program stream url
        DownloadDataJson = dlfunc.download_gzip_json(path.stream_url_program(ProgramId, StreamAssetId))

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
        player.PlayCustom(StreamUrl, listItem, Windowed)
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

        #Get program properties
        ProgramId = listItem.getProperty('ProgramId')
        StreamAssetId = listItem.getProperty('StreamAssetId')

        #Check program properties
        if func.string_isnullorempty(ProgramId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige vod informatie.', notificationIcon, 2500, False)
            return

        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download the program stream url
        DownloadDataJson = dlfunc.download_gzip_json(path.stream_url_vod(ProgramId, StreamAssetId))

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
        player.PlayCustom(StreamUrl, listItem, Windowed)
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

        #Get program properties
        StreamAssetId = listItem.getProperty('StreamAssetId')
        ProgramRecordEventId = listItem.getProperty('ProgramRecordEventId')

        #Check program properties
        if func.string_isnullorempty(ProgramRecordEventId):
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ongeldige opname informatie.', notificationIcon, 2500, False)
            return

        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download the program stream url
        DownloadDataJson = dlfunc.download_gzip_json(path.stream_url_recording(ProgramRecordEventId, StreamAssetId))

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

        #Start playing the media
        player.PlayCustom(StreamUrl, listItem, Windowed)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream afspelen mislukt.', notificationIcon, 2500, False)
