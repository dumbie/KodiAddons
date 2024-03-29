import xbmcgui
import dialog
import files
import func
import getset
import hybrid
import kids
import var
import welcome

def open_settings():
    try:
        #Check kids lock
        if kids.lock_check() == False:
            return

        #Open add-on settings
        var.addon.openSettings()
    except:
        pass

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
    #Get settings
    currentLoginType = getset.setting_get('LoginType')
    currentLoginChecked = getset.setting_get('LoginChecked')
    currentLoginUsername = getset.setting_get('LoginUsername')
    currentLoginPassword = getset.setting_get('LoginPassword')
    currentLoginEmail = getset.setting_get('LoginEmail')
    currentLoginPasswordEmail = getset.setting_get('LoginPasswordEmail')

    #Check settings
    loginNotValid = False
    if currentLoginChecked == 'false':
        loginNotValid = True
    elif currentLoginType == 'Abonnementsnummer' and (func.string_isnullorempty(currentLoginUsername) == True or func.string_isnullorempty(currentLoginPassword) == True):
        loginNotValid = True
    elif currentLoginType == 'Emailadres' and (func.string_isnullorempty(currentLoginEmail) == True or func.string_isnullorempty(currentLoginPasswordEmail) == True):
        loginNotValid = True

    #Open login screen
    if loginNotValid == True:
        return welcome.show_welcome()
    else:
        return True
