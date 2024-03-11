import xbmc
import xbmcgui
import cache
import dialog
import files
import func
import getset
import hybrid
import kids
import path
import var

def reset_global_variables():
    try:
        getset.global_clear('SleepTimer')
    except:
        pass

def kids_change_pincode():
    #Check kids lock
    currentPincode = getset.setting_get('KidsPincode')
    if func.string_isnullorempty(currentPincode) == True or currentPincode != '1234':
        if kids.lock_check() == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kidstongue.png')
            xbmcgui.Dialog().notification(var.addonname, "Helaas pindakaas!", notificationIcon, 2500, False)
            return False

    #Keyboard enter kids pincode
    keyboard = xbmc.Keyboard('default', 'heading')
    keyboard.setHeading('Kids pincode wijzigen')
    keyboard.setDefault('')
    keyboard.setHiddenInput(True)
    keyboard.doModal()
    if keyboard.isConfirmed() == True:
        newPincode = str(keyboard.getText())
        if func.string_isnullorempty(newPincode) == False:
            getset.setting_set('KidsPincode', newPincode)
            xbmcgui.Dialog().notification(var.addonname, "Kids pincode is gewijzigd.", var.addonicon, 2500, False)
        else:
            xbmcgui.Dialog().notification(var.addonname, "Vul een kids pincode in.", var.addonicon, 2500, False)

def switch_kidslock_onoff():
    try:
        #Check kids lock
        if kids.lock_check() == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kidstongue.png')
            xbmcgui.Dialog().notification(var.addonname, "Helaas pindakaas!", notificationIcon, 2500, False)
            return False

        #Switch adult filter setting
        if getset.setting_get('KidsPageLock') == 'false':
            getset.setting_set('KidsPageLock', 'true')
            xbmcgui.Dialog().notification(var.addonname, "Kinder beveiliging ingeschakeld.", var.addonicon, 2500, False)
        else:
            getset.setting_set('KidsPageLock', 'false')
            xbmcgui.Dialog().notification(var.addonname, "Kinder beveiliging uitgeschakeld.", var.addonicon, 2500, False)
    except:
        pass

def switch_adultfilter_onoff():
    try:
        #Check kids lock
        if kids.lock_check() == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kidstongue.png')
            xbmcgui.Dialog().notification(var.addonname, "Helaas pindakaas!", notificationIcon, 2500, False)
            return False

        #Switch adult filter setting
        if getset.setting_get('TelevisionChannelNoErotic') == 'false':
            getset.setting_set('TelevisionChannelNoErotic', 'true')
            xbmcgui.Dialog().notification(var.addonname, "Erotische media uitgeschakeld, herstart de add-on.", var.addonicon, 2500, False)
        else:
            getset.setting_set('TelevisionChannelNoErotic', 'false')
            xbmcgui.Dialog().notification(var.addonname, "Erotische media ingeschakeld, herstart de add-on.", var.addonicon, 2500, False)

        #Remove current cache
        cache.cache_remove_all()
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
