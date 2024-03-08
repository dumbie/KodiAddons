import sys
import xbmcgui
import accent
import argument
import cache
import dialog
import files
import func
import getset
import hybrid
import main
import var

def get_launch_type():
    try:
        str(sys.argv[0])
        str(sys.argv[1])
        str(sys.argv[2])
        return 'Source'
    except:
        return 'Script'

def launch_source():
    check_login_settings()
    cache.cache_check_folder()
    cache.cache_cleanup_all()
    argument.set_launch_argument_source()
    argument.handle_launch_argument_source()

def launch_script():
    if func.check_addon_running() == False:
        func.stop_playing_media()
        reset_global_variables()
        check_login_settings()
        cache.cache_check_folder()
        cache.cache_cleanup_all()
        accent.change_addon_accent()
        main.switch_to_page()
    else:
        func.open_window_id(getset.get_addon_windowId_top())

def reset_global_variables():
    try:
        getset.global_clear('SleepTimer')
    except:
        pass

def reset_thumbnails():
    try:
        dialogAnswers = ["Alle zender logo's vernieuwen"]
        dialogHeader = "Alle zender logo's vernieuwen"
        dialogSummary = "Weet u zeker dat u alle zender logo's wilt vernieuwen? dit zal alle ingeladen afbeeldingen verwijderen zodat de logo's opnieuw gedownload worden."
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == "Alle zender logo's vernieuwen":
            textureFolder = hybrid.string_decode_utf8(hybrid.xbmc_translate_path('special://home/userdata/Thumbnails'))
            files.removeDirectory(textureFolder)
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
            userDirs = files.listDirectoriesUser()
            for userDir in userDirs:
                files.removeDirectoryUser(userDir)

            userFiles = files.listFilesUser()
            for userFile in userFiles:
                if userFile.lower() != 'settings.xml' and userFile.lower() != 'background.png':
                    files.removeFileUser(userFile)

            xbmcgui.Dialog().notification(var.addonname, 'User data bestanden zijn verwijderd.', var.addonicon, 2500, False)
    except:
        pass

def check_login_settings():
    loginNotSet = False
    if func.string_isnullorempty(getset.setting_get('LoginUsername')) == True and func.string_isnullorempty(getset.setting_get('LoginEmail')) == True:
        loginNotSet = True
    elif func.string_isnullorempty(getset.setting_get('LoginPassword')) == True and func.string_isnullorempty(getset.setting_get('LoginPasswordEmail')) == True:
        loginNotSet = True

    if loginNotSet == True:
        xbmcgui.Dialog().notification(var.addonname, 'Stel uw abonnementsgegevens in', var.addonicon, 2500, False)
        var.addon.openSettings()
        return False
    else:
        return True

#Add-on launch
if __name__ == '__main__':
    launchType = get_launch_type()
    if launchType == 'Script':
        launch_script()
    else:
        launch_source()
