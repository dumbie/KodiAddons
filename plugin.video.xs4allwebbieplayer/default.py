import os
import sys
from datetime import datetime, timedelta
import xbmc
import xbmcaddon
import xbmcgui
import alarm
import dialog
import files
import func
import hybrid
import main
import path
import var
import widevine

def check_launch_argument():
    try:
        var.LaunchArgument = sys.argv[1]
        if var.LaunchArgument == "InputAdaptiveSettings":
            xbmcaddon.Addon('inputstream.adaptive').openSettings()
            return False
        elif var.LaunchArgument == "UpdateWidevineFiles":
            widevine.enable_widevine_support(True)
            return False
        elif var.LaunchArgument == "ResetUserdata":
            reset_userdata()
            return False
        elif var.LaunchArgument == "ResetThumbnails":
            reset_thumbnails()
            return False
        return True
    except:
        return True

def reset_thumbnails():
    try:
        dialogAnswers = ["Alle zender logo's vernieuwen"]
        dialogHeader = "Alle zender logo's vernieuwen"
        dialogSummary = "Weet u zeker dat u alle zender logo's wilt vernieuwen? dit zal alle ingeladen afbeeldingen verwijderen zodat de logo's opnieuw gedownload worden."
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == "Alle zender logo's vernieuwen":
            textureFolder = hybrid.string_decode_utf8(xbmc.translatePath('special://home/userdata/Thumbnails'))
            files.removeDirectory(textureFolder)
            xbmc.sleep(100)
            files.createDirectory(textureFolder)
            xbmcgui.Dialog().notification(var.addonname, "Zender logo's zijn verwijderd.", var.addonicon, 2500, False)
    except:
        pass

def reset_userdata():
    try:
        dialogAnswers = ['User data bestanden verwijderen']
        dialogHeader = 'User data bestanden verwijderen'
        dialogSummary = 'Weet u zeker dat u alle user data bestanden van Webbie Player wilt verwijderen? dit kan alleen handig zijn als er een bestand beschadigd is.'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'User data bestanden verwijderen':
            files.removeFileUser('AlarmDataString.js')
            files.removeFileUser('AlarmDataString1.js')
            files.removeFileUser('EpgDataString.js')
            files.removeFileUser('EpgProgramDescriptionString.js')
            files.removeFileUser('EpgProgramDescriptionString1.js')
            files.removeFileUser('EpgProgramDescriptionString2.js')
            files.removeFileUser('ChannelsRadio.js')
            files.removeFileUser('ChannelsTelevision.js')
            files.removeFileUser('FavoriteTelevision.js')
            files.removeFileUser('SearchHistorySearch.js')
            files.removeDirectoryUser('epg')
            xbmcgui.Dialog().notification(var.addonname, 'User data bestanden zijn verwijderd.', var.addonicon, 2500, False)
    except:
        pass

def check_player_status():
    if xbmc.Player().isPlaying():
        xbmc.Player().stop()

def check_multi_launch():
    if var.windowHome.getProperty('WebbiePlayerRunning'):
        lastrunSeconds = float(var.windowHome.getProperty('WebbiePlayerRunning'))
        currentSeconds = float((datetime.now() - datetime(1970,1,1)).total_seconds())
        if (currentSeconds - lastrunSeconds) <= 15:
            xbmcgui.Dialog().notification(var.addonname, 'Webbie Player is al geopend.', var.addonicon, 2500, False)
            return False
        else:
            var.windowHome.setProperty('WebbiePlayerRunning', str(currentSeconds))
            return True
    else:
        currentSeconds = str((datetime.now() - datetime(1970,1,1)).total_seconds())
        var.windowHome.setProperty('WebbiePlayerRunning', currentSeconds)
        return True

def check_login_settings():
    if var.addon.getSetting('LoginUsername') == '' or var.addon.getSetting('LoginPassword') == '':
        var.addon.openSettings()

def stop_addon_threads():
    var.thread_check_requirements = None
    var.thread_refresh_epgtv = None
    var.thread_zap_wait_timer = None
    var.thread_update_information = None
    var.thread_hide_information = None
    var.thread_sleep_timer = None
    var.thread_alarm_timer = None
    var.thread_login_auto = None
    var.thread_clean_epg = None

def reset_home_variables():
    var.windowHome.clearProperty('WebbiePlayerSleepTimer')

def clear_home_variables():
    var.windowHome.clearProperty('WebbiePlayerRunning')
    var.windowHome.clearProperty('WebbiePlayerSleepTimer')

#Change add-on accent to provider
def change_addon_accent():
    #Set image destination paths
    logo = path.resources("resources/skins/default/media/common/logo.png")
    backgroundAddon = path.resources("resources/skins/default/media/common/background_addon.png")
    backgroundAccent = path.resources("resources/skins/default/media/common/background_accent.png")
    scrollbar400 = path.resources("resources/skins/default/media/common/scrollbar_accent_400.png")
    scrollbar800 = path.resources("resources/skins/default/media/common/scrollbar_accent_800.png")

    #Copy provider accent images
    currentProvider = var.addon.getSetting('LoginProvider').lower()
    if currentProvider == 'xs4all':
        files.removeFile(logo)
        files.copyFile(path.resources('resources/skins/default/media/common/logo_xs4all.png'), logo)
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_xs4all.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_xs4all.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_xs4all.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_xs4all.png'), scrollbar800)
    elif currentProvider == 'telfort':
        files.removeFile(logo)
        files.copyFile(path.resources('resources/skins/default/media/common/logo_telfort.png'), logo)
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_telfort.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_telfort.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_telfort.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_telfort.png'), scrollbar800)
    elif currentProvider == 'kpn':
        files.removeFile(logo)
        files.copyFile(path.resources('resources/skins/default/media/common/logo_kpn.png'), logo)
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_kpn.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_kpn.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_kpn.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_kpn.png'), scrollbar800)

    #Copy custom background image
    if files.existFile(path.addonstorage("background.png")):
        files.removeFile(backgroundAddon)
        files.copyFile(path.addonstorage("background.png"), backgroundAddon)

#Add-on launch
if __name__ == '__main__':
    allowLaunch = check_multi_launch()
    argumentLaunch = check_launch_argument()
    if allowLaunch and argumentLaunch:
        reset_home_variables()
        check_player_status()
        check_login_settings()
        change_addon_accent()
        main.switch_to_page()
