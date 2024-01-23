import json
from datetime import datetime, timedelta
import xbmc
import xbmcgui
import apilogin
import re
import func
import hybrid
import metadatainfo
import metadatafunc
import path
import var

def play_stream_radio(listItem):
    try:
        #Get channel properties
        ChannelId = listItem.getProperty('ChannelId')
        ChannelName = listItem.getProperty('ChannelName')
        ChannelStreamUrl = listItem.getProperty('StreamUrl')

        if func.string_isnullorempty(ChannelStreamUrl):
            #Get channel json
            channelJson = metadatafunc.search_channelid_jsonradio(ChannelId)

            #Load channel stream url
            ChannelStreamUrl = channelJson['stream']

        #Update channel settings and variables
        var.addon.setSetting('CurrentRadioId', ChannelId)

        #Update the list item name label
        listItem.setLabel(ChannelName)

        #Start playing the media
        var.PlayerCustom.PlayCustom(ChannelStreamUrl, listItem, True, False)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/radio.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)

def play_stream_recorded(listItem, Windowed):
    #Check if user needs to login
    if apilogin.ApiLogin(False) == False:
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan opname niet openen.', notificationIcon, 2500, False)
        return

    #Download the program stream url
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        #Get and set the stream asset id
        ProgramAssetId = listItem.getProperty('ProgramAssetId')
        ProgramRecordEventId = listItem.getProperty('ProgramRecordEventId')

        #Check the set stream asset id
        if func.string_isnullorempty(ProgramAssetId) or func.string_isnullorempty(ProgramRecordEventId):
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname is niet speelbaar, wegens stream rechten.', notificationIcon, 2500, False)
            return

        DownloadRequest = hybrid.urllib_request(path.stream_url_recording(ProgramRecordEventId, ProgramAssetId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Opname is niet gevonden.', notificationIcon, 2500, False)
        return

    #Check if connection is successful
    if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
        resultCode = DownloadDataJson['resultCode']
        resultMessage = DownloadDataJson['message']
        if resultCode == 'KO':
            var.ApiLoggedIn = False
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opname is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
            return

    #Set stream headers dictionary
    StreamHeadersDict = {
        "User-Agent": var.addon.getSetting('CustomUserAgent')
    }

    #Create stream headers string
    StreamHeaders = ''
    for name, value in StreamHeadersDict.items():
        StreamHeaders += '&' + name + '=' + hybrid.urllib_quote(value)
    StreamHeaders = StreamHeaders.replace('&', '', 1)

    #Get and adjust the stream url
    try:
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']
        if "&max_bitrate=" in StreamUrl:
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetbitrate(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetbitrate()
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Update stream url with localhost proxy
    if xbmc.getCondVisibility('System.Platform.Android') or var.addon.getSetting('UseLocalhostProxy') == 'true':
        StreamUrl = 'http://127.0.0.1:4444/redir/' + StreamUrl

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)
    listItem.setMimeType('application/xml+dash')
    listItem.setContentLookup(False)

    #Get and set stream license key
    try:
        AdaptiveLicenseUrl = DownloadDataJson['resultObj']['src']['sources']['contentProtection']['widevine']['licenseAcquisitionURL']
        AdaptivePostData = 'R{SSM}'
        AdaptiveResponse = ''
        listItem.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
        listItem.setProperty('inputstream.adaptive.license_key', AdaptiveLicenseUrl + "|" + StreamHeaders + "|" + AdaptivePostData + "|" + AdaptiveResponse)
    except:
        pass

    #Update the list item name label
    listItem.setLabel(listItem.getProperty('ProgramName'))

    #Set stream start offset in seconds
    listItem.setProperty('StartOffset', '120')

    #Set internet stream property
    listItem.setProperty("get_stream_details_from_player", 'true')

    #Start playing the media
    var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, False)

def play_stream_program(listItem, Windowed):
    #Check if user needs to login
    if apilogin.ApiLogin(False) == False:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan programma niet openen.', notificationIcon, 2500, False)
        return

    #Get the program id
    ProgramId = listItem.getProperty('ProgramId')

    #Download the program userdata
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.userdata_program(ProgramId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Get and set the stream asset id
        StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(DownloadDataJson['resultObj']['containers'][0]['entitlement']['assets'])

        #Check the set stream asset id
        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Programma is niet speelbaar, wegens stream rechten.', notificationIcon, 2500, False)
            return
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma is niet gevonden.', notificationIcon, 2500, False)
        return

    #Download the program stream url
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.stream_url_program(ProgramId, StreamAssetId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Programma is niet gevonden.', notificationIcon, 2500, False)
        return

    #Check if connection is successful
    if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
        resultCode = DownloadDataJson['resultCode']
        resultMessage = DownloadDataJson['message']
        if resultCode == 'KO':
            var.ApiLoggedIn = False
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Programma is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
            return

    #Set stream headers dictionary
    StreamHeadersDict = {
        "User-Agent": var.addon.getSetting('CustomUserAgent')
    }

    #Create stream headers string
    StreamHeaders = ''
    for name, value in StreamHeadersDict.items():
        StreamHeaders += '&' + name + '=' + hybrid.urllib_quote(value)
    StreamHeaders = StreamHeaders.replace('&', '', 1)

    #Get and adjust the stream url
    try:
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']
        if "&max_bitrate=" in StreamUrl:
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetbitrate(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetbitrate()
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Update stream url with localhost proxy
    if xbmc.getCondVisibility('System.Platform.Android') or var.addon.getSetting('UseLocalhostProxy') == 'true':
        StreamUrl = 'http://127.0.0.1:4444/redir/' + StreamUrl

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)
    listItem.setMimeType('application/xml+dash')
    listItem.setContentLookup(False)

    #Get and set stream license key
    try:
        AdaptiveLicenseUrl = DownloadDataJson['resultObj']['src']['sources']['contentProtection']['widevine']['licenseAcquisitionURL']
        AdaptivePostData = 'R{SSM}'
        AdaptiveResponse = ''
        listItem.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
        listItem.setProperty('inputstream.adaptive.license_key', AdaptiveLicenseUrl + "|" + StreamHeaders + "|" + AdaptivePostData + "|" + AdaptiveResponse)
    except:
        pass

    #Update the list item name label
    listItem.setLabel(listItem.getProperty('ProgramName'))

    #Set stream start offset in seconds
    listItem.setProperty('StartOffset', '120')

    #Set internet stream property
    listItem.setProperty("get_stream_details_from_player", 'true')

    #Start playing the media
    var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, False)

def play_stream_vod(listItem, Windowed):
    #Check if user needs to login
    if apilogin.ApiLogin(False) == False:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan vod niet openen.', notificationIcon, 2500, False)
        return

    ProgramId = listItem.getProperty('ProgramId')

    #Download the program userdata
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.userdata_vod(ProgramId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Get and set the stream asset id
        StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(DownloadDataJson['resultObj']['containers'][0]['entitlement']['assets'])

        #Check the set stream asset id
        if func.string_isnullorempty(StreamAssetId):
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Vod is niet speelbaar, wegens stream rechten.', notificationIcon, 2500, False)
            return
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Vod is niet gevonden.', notificationIcon, 2500, False)
        return

    #Download the program stream url
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        DownloadRequest = hybrid.urllib_request(path.stream_url_vod(ProgramId, StreamAssetId), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Vod is niet gevonden.', notificationIcon, 2500, False)
        return

    #Check if connection is successful
    if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
        resultCode = DownloadDataJson['resultCode']
        resultMessage = DownloadDataJson['message']
        if resultCode == 'KO':
            var.ApiLoggedIn = False
            notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
            xbmcgui.Dialog().notification(var.addonname, 'Vod is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
            return

    #Set stream headers dictionary
    StreamHeadersDict = {
        "User-Agent": var.addon.getSetting('CustomUserAgent')
    }

    #Create stream headers string
    StreamHeaders = ''
    for name, value in StreamHeadersDict.items():
        StreamHeaders += '&' + name + '=' + hybrid.urllib_quote(value)
    StreamHeaders = StreamHeaders.replace('&', '', 1)

    #Get and adjust the stream url
    try:
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']
        if "&max_bitrate=" in StreamUrl:
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetbitrate(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetbitrate()
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Update stream url with localhost proxy
    if xbmc.getCondVisibility('System.Platform.Android') or var.addon.getSetting('UseLocalhostProxy') == 'true':
        StreamUrl = 'http://127.0.0.1:4444/redir/' + StreamUrl

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)
    listItem.setMimeType('application/xml+dash')
    listItem.setContentLookup(False)

    #Get and set stream license key
    try:
        AdaptiveLicenseUrl = DownloadDataJson['resultObj']['src']['sources']['contentProtection']['widevine']['licenseAcquisitionURL']
        AdaptivePostData = 'R{SSM}'
        AdaptiveResponse = ''
        listItem.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
        listItem.setProperty('inputstream.adaptive.license_key', AdaptiveLicenseUrl + "|" + StreamHeaders + "|" + AdaptivePostData + "|" + AdaptiveResponse)
    except:
        pass

    #Update the list item name label
    listItem.setLabel(listItem.getProperty('ProgramName'))

    #Set internet stream property
    listItem.setProperty("get_stream_details_from_player", 'true')

    #Start playing the media
    var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, False)

def play_stream_television(listItem, Windowed, SeekOffset=0):
    #Check if user needs to login
    if apilogin.ApiLogin(False) == False:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Niet aangemeld, kan zender niet openen.', notificationIcon, 2500, False)
        return

    #Get channel properties
    NewAssetId = listItem.getProperty('AssetId')
    NewChannelId = listItem.getProperty('ChannelId')
    NewExternalId = listItem.getProperty('ExternalId')
    NewChannelName = listItem.getProperty('ChannelName')

    #Check channel asset identifier
    if func.string_isnullorempty(NewAssetId):
        NewAssetId = metadatafunc.search_stream_assetid_by_channelid(NewChannelId)

    #Check channel asset identifier
    if func.string_isnullorempty(NewAssetId):
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zender asset id niet gevonden.', notificationIcon, 2500, False)
        return

    #Allow longer back seeking
    DateTimeUtc = datetime.utcnow() - timedelta(minutes=400)
    StartString = '&time=' + str(func.datetime_to_ticks(DateTimeUtc))

    #Download the television stream url
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie,
            "X-Xsrf-Token": var.ApiLoginToken
        }

        RequestUrl = path.stream_url_tv(NewChannelId, NewAssetId) + StartString
        DownloadRequest = hybrid.urllib_request(RequestUrl, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zender is niet gevonden.', notificationIcon, 2500, False)
        return

    #Check if connection is successful
    if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
        resultCode = DownloadDataJson['resultCode']
        resultMessage = DownloadDataJson['message']
        if resultCode == 'KO':
            var.ApiLoggedIn = False
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Zender is niet beschikbaar: ' + resultMessage, notificationIcon, 2500, False)
            return

    #Set stream headers dictionary
    StreamHeadersDict = {
        "User-Agent": var.addon.getSetting('CustomUserAgent')
    }

    #Create stream headers string
    StreamHeaders = ''
    for name, value in StreamHeadersDict.items():
        StreamHeaders += '&' + name + '=' + hybrid.urllib_quote(value)
    StreamHeaders = StreamHeaders.replace('&', '', 1)

    #Get and adjust the stream url
    try:
        StreamUrl = DownloadDataJson['resultObj']['src']['sources']['src']
        StreamUrl = StreamUrl.replace('/Manifest?', '/.mpd?')
        if "&max_bitrate=" in StreamUrl:
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetbitrate(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetbitrate()
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Download mpd to gain access to no drm stream
    try:
        DownloadRequest = hybrid.urllib_request(StreamUrl, headers=StreamHeadersDict)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        StreamUrl = StreamUrl.replace('v.isml/', 'n.isml/')
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream zonder DRM is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Update stream url with localhost proxy
    if xbmc.getCondVisibility('System.Platform.Android') or var.addon.getSetting('UseLocalhostProxy') == 'true':
        StreamUrl = 'http://127.0.0.1:4444/redir/' + StreamUrl

    #Update channel settings and variables
    CurrentChannelId = var.addon.getSetting('CurrentChannelId')
    CurrentExternalId = var.addon.getSetting('CurrentExternalId')
    CurrentChannelName = var.addon.getSetting('CurrentChannelName')
    if CurrentChannelId != NewChannelId:
        var.addon.setSetting('LastChannelId', CurrentChannelId)
        var.addon.setSetting('LastExternalId', CurrentExternalId)
        var.addon.setSetting('LastChannelName', CurrentChannelName)
    var.addon.setSetting('CurrentChannelId', NewChannelId)
    var.addon.setSetting('CurrentExternalId', NewExternalId)
    var.addon.setSetting('CurrentChannelName', NewChannelName)

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)
    listItem.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
    listItem.setMimeType('application/xml+dash')
    listItem.setContentLookup(False)

    #Get and set stream license key
    try:
        AdaptiveLicenseUrl = DownloadDataJson['resultObj']['src']['sources']['contentProtection']['widevine']['licenseAcquisitionURL']
        AdaptivePostData = 'R{SSM}'
        AdaptiveResponse = ''
        listItem.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
        listItem.setProperty('inputstream.adaptive.license_key', AdaptiveLicenseUrl + "|" + StreamHeaders + "|" + AdaptivePostData + "|" + AdaptiveResponse)
    except:
        pass

    #Update the list item name label
    listItem.setLabel(NewChannelName)

    #Set internet stream property
    listItem.setProperty("get_stream_details_from_player", 'true')

    #Start playing the media
    var.PlayerCustom.PlayCustom(StreamUrl, listItem, Windowed, True, SeekOffset)
