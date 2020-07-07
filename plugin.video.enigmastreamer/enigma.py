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
def enigma_list_channels(e2servicereference):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    RequestUrl = 'http://' + SettingHost + '/web/getservices?sRef=' + hybrid.urllib_quote(e2servicereference)
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
def enigma_epg_information(e2servicereference):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    RequestUrl = 'http://' + SettingHost + '/web/epgservicenow?sRef=' + hybrid.urllib_quote(e2servicereference)
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
    e2servicename = listItem.getProperty('e2servicename')
    e2servicereference = listItem.getProperty('e2servicereference')

    #Check if channel is a bouquet
    if e2servicereference.startswith('1:64:'):
        return
    #Check if channel is a webstream
    elif enigma_check_webstream(e2servicereference):
        e2servicereference = enigma_get_webstreamurl(e2servicereference)
    else:
        e2servicereference = 'http://' + SettingHost + ':8001/' + e2servicereference

    listItem.setLabel(e2servicename)
    xbmc.Player().play(e2servicereference, listItem)

#Enigma stream recording
def enigma_stream_recording(listItem):
    #Check the current settings
    SettingHost = var.addon.getSetting('host')
    if SettingHost.endswith('.') or SettingHost.endswith('0') or not SettingHost[-1].isdigit():
        notificationIcon = func.path_resources('resources/skins/default/media/common/settings.png')
        xbmcgui.Dialog().notification(var.addonname, 'Please check the ip address.', notificationIcon, 2500, False)
        return

    #Get the stream reference
    e2title = listItem.getProperty('e2title')
    e2filename = listItem.getProperty('e2filename')

    #Set the stream uri
    streamUri = 'http://' + SettingHost + '/file?file=' + e2filename

    listItem.setLabel(e2title)
    xbmc.Player().play(streamUri, listItem)

#Check if service is web stream
def enigma_check_webstream(e2servicereference):
    if e2servicereference.startswith('4097:') or e2servicereference.startswith('5001:') or e2servicereference.startswith('5002:'):
        return True
    return False

#Get enigma web stream url
def enigma_get_webstreamurl(e2servicereference):
    streamUrl = e2servicereference[23:]
    lastSplit = streamUrl.count(':') 
    return func.string_remove_after_char(streamUrl, ':', lastSplit)
