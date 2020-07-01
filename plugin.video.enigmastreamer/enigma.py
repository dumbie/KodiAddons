import xml.etree.ElementTree as ET
import func
import hybrid
import var
import xbmc
import xbmcgui

#Enigma list bouquets
def enigma_list_bouquets():
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    RequestUrl = 'http://' + SettingHost + '/web/getservices'
    DownloadDataHttp = hybrid.urllib_urlopen(RequestUrl)
    DownloadDataString = DownloadDataHttp.read()
    DownloadDataXml = ET.ElementTree(ET.fromstring(DownloadDataString))
    return DownloadDataXml

#Enigma list channels
def enigma_list_channels(bouquetId):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    RequestUrl = 'http://' + SettingHost + '/web/getservices?sRef=' + hybrid.urllib_quote(bouquetId)
    DownloadDataHttp = hybrid.urllib_urlopen(RequestUrl)
    DownloadDataString = DownloadDataHttp.read()
    DownloadDataXml = ET.ElementTree(ET.fromstring(DownloadDataString))
    return DownloadDataXml

#Enigma list recordings
def enigma_list_recordings():
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    RequestUrl = 'http://' + SettingHost + '/web/movielist'
    DownloadDataHttp = hybrid.urllib_urlopen(RequestUrl)
    DownloadDataString = DownloadDataHttp.read()
    DownloadDataXml = ET.ElementTree(ET.fromstring(DownloadDataString))
    return DownloadDataXml

#Enigma epg information
def enigma_epg_information(channelId):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    RequestUrl = 'http://' + SettingHost + '/web/epgservicenow?sRef=' + hybrid.urllib_quote(channelId)
    DownloadDataHttp = hybrid.urllib_urlopen(RequestUrl)
    DownloadDataString = DownloadDataHttp.read()
    DownloadDataXml = ET.ElementTree(ET.fromstring(DownloadDataString))
    return DownloadDataXml

#Enigma receiver standby
def enigma_receiver_standby():
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    try:
        RequestUrl = 'http://' + SettingHost + '/web/powerstate?newstate=5'
        hybrid.urllib_urlopen(RequestUrl)
        notificationIcon = func.path_resources('resources/skins/default/media/common/shutdown.png')
        xbmcgui.Dialog().notification(var.addonname, 'Receiver is now in standby.', notificationIcon, 2500, False)
    except:
        notificationIcon = func.path_resources('resources/skins/default/media/common/shutdown.png')
        xbmcgui.Dialog().notification(var.addonname, 'Failed to put receiver in standby.', notificationIcon, 2500, False)
        return

#Enigma stream channel
def enigma_stream_channel(listItem):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    #Get the stream reference
    streamName = listItem.getProperty('e2servicename')
    streamName = hybrid.urllib_unquote(streamName)
    streamUri = listItem.getProperty('e2servicereference')
    streamUri = hybrid.urllib_unquote(streamUri)

    #Check if channel is a bouquet
    if streamUri.startswith('1:64:'):
        return
    #Check if channel is a webstream
    elif streamUri.startswith('4097:') or streamUri.startswith('5001:') or streamUri.startswith('5002:'):
        streamUri = streamUri[23:]
        streamUri = streamUri.replace(':' + streamName,'')
    else:
        streamUri = 'http://' + SettingHost + ':8001/' + streamUri

    listItem.setLabel(streamName)
    xbmc.Player().play(streamUri, listItem)

#Enigma stream recording
def enigma_stream_recording(listItem):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    #Get the stream reference
    streamName = listItem.getProperty('e2title')
    streamName = hybrid.urllib_unquote(streamName)
    streamFile = listItem.getProperty('e2filename')
    streamFile = hybrid.urllib_quote(streamFile)

    #Set the stream uri
    streamUri = 'http://' + SettingHost + '/file?file=' + streamFile

    listItem.setLabel(streamName)
    xbmc.Player().play(streamUri, listItem)
