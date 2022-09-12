import json
from datetime import datetime, timedelta
import xbmcgui
import apilogin
import re
import func
import hybrid
import metadatainfo
import path
import var

#Switch to a new channel by listitem
def switch_channel_tv_listitem(listitem, Windowed=False, showInformation=False, SeekOffset=0):
    play_stream_television(listitem, Windowed, SeekOffset)

    if showInformation and var.guiPlayer != None:
        var.guiPlayer.show_epg(True)

#Switch to a new channel by id
def switch_channel_tv_channelid(AssetId, ChannelId, ExternalId, ChannelName='Onbekende zender', Genre='Onbekend', Windowed=False, showInformation=False):
    if func.string_isnullorempty(AssetId) or func.string_isnullorempty(ChannelId) or func.string_isnullorempty(ExternalId):
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Ongeldige zender informatie.', notificationIcon, 2500, False)
        return

    if func.string_isnullorempty(ChannelName):
        ChannelName = 'Onbekende zender'

    if func.string_isnullorempty(Genre):
        Genre = 'Onbekend'

    listitem = xbmcgui.ListItem()
    listitem.setProperty('AssetId', AssetId)
    listitem.setProperty('ChannelId', ChannelId)
    listitem.setProperty('ExternalId', ExternalId)
    listitem.setProperty('ChannelName', ChannelName)
    listitem.setInfo('video', {'Genre': Genre})
    play_stream_television(listitem, Windowed)

    if showInformation and var.guiPlayer != None:
        var.guiPlayer.show_epg(True)

def play_stream_radio(listItem):
    #Update channel settings and variables
    var.addon.setSetting('CurrentRadioId', listItem.getProperty('ChannelId'))

    #Update the list item name label
    listItem.setLabel(listItem.getProperty('ChannelName'))

    #Start playing the media
    var.PlayerCustom.PlayCustom(listItem.getProperty('StreamUrl'), listItem, True, False)

def play_stream_recorded(listItem, Windowed):
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

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
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetresolution(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetresolution()
        StreamUrl += '&drm=clear'
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)

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
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

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
        StreamAssetId = metadatainfo.get_stream_assetid(DownloadDataJson['resultObj']['containers'][0]['entitlement']['assets'])

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
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetresolution(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetresolution()
        StreamUrl += '&drm=clear'
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)

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
    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

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
        StreamAssetId = metadatainfo.get_stream_assetid(DownloadDataJson['resultObj']['containers'][0]['entitlement']['assets'])

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
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetresolution(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetresolution()
        StreamUrl += '&drm=clear'
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/vodno.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)

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
    #Get channel settings and variables
    NewAssetId = listItem.getProperty('AssetId')
    NewChannelId = listItem.getProperty('ChannelId')
    NewExternalId = listItem.getProperty('ExternalId')
    NewChannelName = listItem.getProperty('ChannelName')
    CurrentAssetId = var.addon.getSetting('CurrentAssetId')
    CurrentChannelId = var.addon.getSetting('CurrentChannelId')
    CurrentExternalId = var.addon.getSetting('CurrentExternalId')
    CurrentChannelName = var.addon.getSetting('CurrentChannelName')

    #Allow longer back seeking
    DateTimeUtc = datetime.utcnow() - timedelta(minutes=400)
    StartString = '&time=' + str(func.datetime_to_ticks(DateTimeUtc))

    #Check if user is logged in
    if var.ApiLoggedIn == False:
        apilogin.ApiLogin(False)

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
        if "&max_bitrate=" in StreamUrl:
            StreamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.get_stream_targetresolution(), StreamUrl)
        else:
            StreamUrl += "&max_bitrate=" + metadatainfo.get_stream_targetresolution()
        StreamUrl += '&drm=clear'
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/television.png')
        xbmcgui.Dialog().notification(var.addonname, 'Stream is niet beschikbaar.', notificationIcon, 2500, False)
        return

    #Update channel settings and variables
    if CurrentChannelId != NewChannelId:
        var.addon.setSetting('LastAssetId', CurrentAssetId)
        var.addon.setSetting('LastChannelId', CurrentChannelId)
        var.addon.setSetting('LastExternalId', CurrentExternalId)
        var.addon.setSetting('LastChannelName', CurrentChannelName)

    var.addon.setSetting('CurrentAssetId', NewAssetId)
    var.addon.setSetting('CurrentChannelId', NewChannelId)
    var.addon.setSetting('CurrentExternalId', NewExternalId)
    var.addon.setSetting('CurrentChannelName', NewChannelName)

    #Set input adaptive stream
    listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
    listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeaders)
    listItem.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')

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
