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

    downloadUri = 'http://' + SettingHost + '/web/getservices'
    DownloadDataHttp = urllib2.urlopen(downloadUri)
    DownloadDataHttp = DownloadDataHttp.read()
    DownloadDataXml = ET.ElementTree(ET.fromstring(DownloadDataHttp))
    return DownloadDataXml

#Enigma list channels
def enigma_list_channels(bouquetId):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    downloadUri = 'http://' + SettingHost + '/web/getservices?sRef=' + urllib2.quote(bouquetId)
    DownloadDataHttp = urllib2.urlopen(downloadUri)
    DownloadDataHttp = DownloadDataHttp.read()
    DownloadDataXml = ET.ElementTree(ET.fromstring(DownloadDataHttp))
    return DownloadDataXml

#Enigma epg information
def enigma_epg_information(channelId):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    downloadUri = 'http://' + SettingHost + '/web/epgservicenow?sRef=' + urllib2.quote(channelId)
    DownloadDataHttp = urllib2.urlopen(downloadUri)
    DownloadDataHttp = DownloadDataHttp.read()
    DownloadDataXml = ET.ElementTree(ET.fromstring(DownloadDataHttp))
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
        downloadUri = 'http://' + SettingHost + '/web/powerstate?newstate=5'
        urllib2.urlopen(downloadUri)
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
    streamUri = listItem.getProperty('e2servicereference')

    #Check if channel is a webstream
    if streamUri.startswith('4097:0:1:0:0:0:0:0:0:0:'):
        streamUri = streamUri.replace('4097:0:1:0:0:0:0:0:0:0:','')
        streamUri = streamUri.replace(':' + streamName,'')
        streamUri = urllib2.unquote(streamUri)
    elif streamUri.startswith('1:64:0:0:0:0:0:0:0:0:'):
        return
    else:
        streamUri = urllib2.quote(streamUri)
        streamUri = 'http://' + SettingHost + ':8001/' + streamUri

    listItem.setLabel(streamName)
    xbmc.Player().play(streamUri, listItem)
