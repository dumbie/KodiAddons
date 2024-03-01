import sys
import xbmcgui
import argument
import dialog
import files
import func
import getset
import hybrid
import main
import path
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
    argument.set_launch_argument_source()
    argument.handle_launch_argument_source()

def launch_script():
    if func.check_addon_running() == False:
        func.stop_playing_media()
        reset_global_variables()
        check_login_settings()
        change_addon_accent()
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
                if userFile != 'settings.xml':
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

#Change add-on accent images
def change_addon_accent():
    #Set image destination paths
    backgroundAddon = path.resources("resources/skins/default/media/common/background_addon.png")
    backgroundAccent = path.resources("resources/skins/default/media/common/background_accent.png")
    scrollbar400 = path.resources("resources/skins/default/media/common/scrollbar_accent_400.png")
    scrollbar800 = path.resources("resources/skins/default/media/common/scrollbar_accent_800.png")

    #Copy add-on accent images
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_yellow.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_yellow.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_yellow.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_yellow.png'), scrollbar800)
    elif currentProvider == 'blauw':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_blue.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_blue.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_blue.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_blue.png'), scrollbar800)
    elif currentProvider == 'groen':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_green.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_green.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_green.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_green.png'), scrollbar800)
    elif currentProvider == 'grijs':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_gray.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_gray.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_gray.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_gray.png'), scrollbar800)

    #Copy custom background image
    if files.existFileUser(path.addonstorage("background.png")):
        files.removeFile(backgroundAddon)
        files.copyFile(path.addonstorage("background.png"), backgroundAddon)

#Add-on launch
if __name__ == '__main__':
    launchType = get_launch_type()
    if launchType == 'Script':
        launch_script()
    else:
        launch_source()
