import json
import os
import platform
from zipfile import ZipFile
import xbmc
import xbmcaddon
import xbmcgui
import func
import hybrid
import path
import var

def thread_check_requirements():
    enable_inputstreamadaptive()
    if var.addon.getSetting('InputAdaptiveAdjust') == 'true':
        adjust_inputstreamadaptive()
    enable_widevine_support()

def enable_inputstreamadaptive():
    failed = False
    try:
        JSONRPC = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'Addons.SetAddonEnabled',
            'params':
            {
                'addonid': 'inputstream.adaptive',
                'enabled': True
            }
        }
        result = xbmc.executeJSONRPC(json.dumps(JSONRPC))
        if 'error' in result:
            failed = True
    except:
        failed = True
    if failed == True:
        xbmcgui.Dialog().notification(var.addonname, 'Inputstream add-on inschakelen mislukt.', var.addonicon, 2500, False)

def adjust_inputstreamadaptive():
    try:
        input_addon = xbmcaddon.Addon('inputstream.adaptive')
        input_addon.setSetting('MAXRESOLUTION', '4')
        input_addon.setSetting('MAXRESOLUTIONSECURE', '4')
        input_addon.setSetting('IGNOREDISPLAY', 'true')
    except:
        xbmcgui.Dialog().notification(var.addonname, 'Inputstream add-on instellen mislukt.', var.addonicon, 2500, False)

def enable_widevine_support(forceUpdate=False):
    #Check if Widevine is already updating
    if var.WidevineUpdating == True: return
    var.WidevineUpdating = True

    #Get InputStream adaptive Widevine path
    input_addon = xbmcaddon.Addon('inputstream.adaptive')
    decrypter_path = input_addon.getSetting('DECRYPTERPATH')
    if func.string_isnullorempty(decrypter_path):
        widevine_path = hybrid.string_decode_utf8(hybrid.xbmc_translate_path('special://home/cdm'))
        input_addon.setSetting('DECRYPTERPATH', 'special://home/cdm')
    else:
        widevine_path = hybrid.string_decode_utf8(hybrid.xbmc_translate_path(decrypter_path))

    #Set the download headers
    DownloadHeaders = {
        "User-Agent": var.addon.getSetting('CustomUserAgent')
    }

    #Check if newer Widevine version is available
    RequestUrl = str(path.requirements()) + 'version.txt'
    DownloadRequest = hybrid.urllib_request(RequestUrl, headers=DownloadHeaders)
    DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
    DownloadDataString = DownloadDataHttp.read().decode()
    if DownloadDataString != var.addon.getSetting('WidevineVersion'):
        var.addon.setSetting('WidevineVersion', DownloadDataString)
        forceUpdate = True

    #Check if Widevine support is installed
    if forceUpdate == False:
        for aRoot, aDirs, aFiles in os.walk(widevine_path):
            for fileName in aFiles:
                if 'widevinecdm' in fileName:
                    var.WidevineUpdating = False
                    return

    #Check the system processor architecture
    downloadArchitecture = ''
    systemArchitecture = platform.machine().lower()
    systemBits = platform.architecture()[0].lower()
    if 'arm' in systemArchitecture: downloadArchitecture = 'arm'
    elif systemBits == '32bit': downloadArchitecture = 'x86'
    elif systemBits == '64bit': downloadArchitecture = 'x64'

    #Check if operating system is supported
    downloadOperatingSystem = ''
    if xbmc.getCondVisibility('System.Platform.Android'):
        var.WidevineUpdating = False
        return
    elif xbmc.getCondVisibility('System.Platform.IOS'):
        var.WidevineUpdating = False
        return
    elif xbmc.getCondVisibility('System.Platform.Linux'):
        downloadOperatingSystem = 'linux'
    elif xbmc.getCondVisibility('System.Platform.OSX'):
        downloadOperatingSystem = 'mac'
    elif xbmc.getCondVisibility('System.Platform.Windows'):
        downloadOperatingSystem = 'win'
    else:
        var.WidevineUpdating = False
        xbmcgui.Dialog().notification(var.addonname, 'Besturing systeem wordt niet ondersteund.', var.addonicon, 2500, False)
        return

    #Notify the user Widevine is installing
    xbmcgui.Dialog().notification(var.addonname, 'Widevine wordt geinstalleerd.', var.addonicon, 2500, False)

    #Stop the current playback of any media
    if xbmc.Player().isPlaying():
        xbmc.Player().stop()
        xbmc.sleep(1000)

    #Create the Widevine decrypter directory
    if os.path.exists(widevine_path) == False:
        os.mkdir(widevine_path)

    try:
        #Download the required Widevine files
        RequestUrl = str(path.requirements()) + 'widevine-' + str(downloadOperatingSystem) + '-' + str(downloadArchitecture) + '.zip'
        DownloadRequest = hybrid.urllib_request(RequestUrl, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataBytes = DownloadDataHttp.read()

        #Write the downloaded Widevine zip file
        download_filename = widevine_path + '/widevine.zip'
        filewrite = open(download_filename, 'wb')
        filewrite.write(DownloadDataBytes)
        filewrite.close()
    except:
        var.WidevineUpdating = False
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Mislukt om Widevine te downloaden.', notificationIcon, 2500, False)
        return

    try:
        #Extract the downloaded Widevine zip file
        downloadZip = ZipFile(download_filename)
        downloadZip.extractall(widevine_path)
        downloadZip.close()
    except:
        var.WidevineUpdating = False
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Mislukt om Widevine te installeren.', notificationIcon, 2500, False)
        return

    #Remove the downloaded Widevine zip file
    os.remove(download_filename)

    var.WidevineUpdating = False
    xbmcgui.Dialog().notification(var.addonname, 'Widevine is succesvol geinstalleerd.', var.addonicon, 2500, False)
