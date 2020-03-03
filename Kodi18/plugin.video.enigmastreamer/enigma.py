import urllib2
import xml.etree.ElementTree as ET
import func
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
    DownloadDataHttp = urllib2.urlopen(RequestUrl)
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

    RequestUrl = 'http://' + SettingHost + '/web/getservices?sRef=' + urllib2.quote(bouquetId)
    DownloadDataHttp = urllib2.urlopen(RequestUrl)
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

    RequestUrl = 'http://' + SettingHost + '/web/epgservicenow?sRef=' + urllib2.quote(channelId)
    DownloadDataHttp = urllib2.urlopen(RequestUrl)
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
        urllib2.urlopen(RequestUrl)
        notificationIcon = func.path_resources('resources/skins/default/media/common/shutdown.png')
        xbmcgui.Dialog().notification(var.addonname, 'Receiver is now in standby.', notificationIcon, 2500, False)
    except:
        notificationIcon = func.path_resources('resources/skins/default/media/common/shutdown.png')
        xbmcgui.Dialog().notification(var.addonname, 'Failed to put receiver in standby.', notificationIcon, 2500, False)
        return

#Enigma stream channel
def enigma_stream(listItem):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    #Get the stream reference
    streamName = listItem.getProperty('e2servicename')
    streamName = urllib2.unquote(streamName)
    streamUri = listItem.getProperty('e2servicereference')
    streamUri = urllib2.unquote(streamUri)

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
