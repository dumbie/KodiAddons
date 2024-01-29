import json
from datetime import datetime, timedelta
import xbmcgui
import apilogin
import func
import hybrid
import metadatainfo
import path
import streamadjust
import streamcheck
import var

def play_tv(listItem, Windowed, ShowInformation=False, SeekOffsetEnd=0):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Check channel properties
        streamcheck.check_tv(listItem)

        #Get channel properties
        NewAssetId = listItem.getProperty('AssetId')
        NewChannelId = listItem.getProperty('ChannelId')

        #Check the set stream asset id
        if func.string_isnullorempty(NewAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Allow longer back seeking
        DateTimeUtc = datetime.utcnow() - timedelta(minutes=400)
        StartString = '&time=' + str(func.datetime_to_ticks(DateTimeUtc))

        #Download the television stream url
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            "X-Xsrf-Token": var.ApiLoginToken()
        }

        RequestUrl = path.stream_url_tv(NewChannelId, NewAssetId) + StartString
        DownloadRequest = hybrid.urllib_request(RequestUrl, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

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

        #Get the downloaded stream url
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
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, True, ShowInformation, SeekOffsetEnd=SeekOffsetEnd)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)

def play_radio(listItem, Windowed):
    try:
        #Check channel properties
        streamcheck.check_radio(listItem)

        #Get channel properties
        ChannelId = listItem.getProperty('ChannelId')
        ChannelStreamUrl = listItem.getProperty('StreamUrl')

        #Update channel settings and variables
        var.addon.setSetting('CurrentRadioId', ChannelId)

        #Start playing the media
        var.PlayerCustom.PlayCustom(ChannelStreamUrl, listItem, Windowed)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)

def play_program(listItem, Windowed, SeekOffsetStart=120):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Get the program id
        ProgramId = listItem.getProperty('ProgramId')

        #Download the program userdata
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            "X-Xsrf-Token": var.ApiLoginToken()
        }

        DownloadRequest = hybrid.urllib_request(path.userdata_program(ProgramId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Get and set the stream asset id
        StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(DownloadDataJson['resultObj']['containers'][0]['entitlement']['assets'])

        #Check the set stream asset id
        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download the program stream url
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            "X-Xsrf-Token": var.ApiLoginToken()
        }

        DownloadRequest = hybrid.urllib_request(path.stream_url_program(ProgramId, StreamAssetId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

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
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, SeekOffsetStart=SeekOffsetStart)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)

def play_vod(listItem, Windowed):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        ProgramId = listItem.getProperty('ProgramId')

        #Download the program userdata
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            "X-Xsrf-Token": var.ApiLoginToken()
        }

        DownloadRequest = hybrid.urllib_request(path.userdata_vod(ProgramId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Get and set the stream asset id
        StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(DownloadDataJson['resultObj']['containers'][0]['entitlement']['assets'])

        #Check the set stream asset id
        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download the program stream url
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            "X-Xsrf-Token": var.ApiLoginToken()
        }

        DownloadRequest = hybrid.urllib_request(path.stream_url_vod(ProgramId, StreamAssetId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

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
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)

def play_recorded(listItem, Windowed, SeekOffsetStart=120):
    try:
        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan stream niet openen.', notificationIcon, 2500, False)
            return

        #Get and set the stream asset id
        ProgramAssetId = listItem.getProperty('ProgramAssetId')
        ProgramRecordEventId = listItem.getProperty('ProgramRecordEventId')

        #Check the set stream asset id
        if func.string_isnullorempty(ProgramAssetId) or func.string_isnullorempty(ProgramRecordEventId):
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Stream is niet speelbaar wegens rechten.', notificationIcon, 2500, False)
            return

        #Download the program stream url
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            "X-Xsrf-Token": var.ApiLoginToken()
        }

        DownloadRequest = hybrid.urllib_request(path.stream_url_recording(ProgramRecordEventId, ProgramAssetId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

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
        var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, SeekOffsetStart=SeekOffsetStart)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
