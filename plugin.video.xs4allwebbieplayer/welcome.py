import xbmc
import xbmcgui
import apilogin
import func
import getset
import guifunc
import var

def show_welcome():
    if var.guiWelcome == None:
        var.guiWelcome = Gui('welcome.xml', var.addonpath, 'default', '720p')
        var.guiWelcome.setProperty('WebbiePlayerPage', 'Open')
        var.guiWelcome.show()

        var.WelcomeResult = None
        while var.WelcomeResult == None and func.check_loop_allowed():
            xbmc.sleep(100)

        return var.WelcomeResult

def close_welcome(setWelcomeResult):
    if var.guiWelcome != None:
        #Set the Welcome chosen result
        var.WelcomeResult = setWelcomeResult

        #Close the shown window
        var.guiWelcome.close()
        var.guiWelcome = None

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Load current login settings
        self.load_settings()

        #Focus on interface
        guifunc.controlFocus(self, 1001)

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_welcome(False)

    def onClick(self, clickId):
        if clickId == 1001:
            guifunc.updateRadioSelection(self, 1004, False)
        elif clickId == 1004:
            guifunc.updateRadioSelection(self, 1001, False)
        elif clickId == 1007:
            self.save_settings()
        elif clickId == 1008:
            close_welcome(False)

    def load_settings(self):
        #Load settings
        if getset.setting_get('LoginType') == 'Abonnementsnummer':
            guifunc.updateRadioSelection(self, 1004, False)
            guifunc.updateRadioSelection(self, 1001, True)
        else:
            guifunc.updateRadioSelection(self, 1004, True)
            guifunc.updateRadioSelection(self, 1001, False)
        guifunc.updateTextBoxText(self, 1002, getset.setting_get('LoginUsername'))
        guifunc.updateTextBoxText(self, 1003, getset.setting_get('LoginPassword'))
        guifunc.updateTextBoxText(self, 1005, getset.setting_get('LoginEmail'))
        guifunc.updateTextBoxText(self, 1006, getset.setting_get('LoginPasswordEmail'))

    def save_settings(self):
        #Get settings
        newLoginTypeAbonnementsnummer = self.getControl(1001).isSelected()
        newLoginUsername = self.getControl(1002).getText().replace(' ', '')
        newLoginPassword = self.getControl(1003).getText().replace(' ', '')
        newLoginTypeEmailadres = self.getControl(1004).isSelected()
        newLoginEmail = self.getControl(1005).getText().replace(' ', '')
        newLoginPasswordEmail = self.getControl(1006).getText().replace(' ', '')

        #Check settings
        if newLoginTypeEmailadres == False and newLoginTypeAbonnementsnummer == False:
            xbmcgui.Dialog().notification(var.addonname, "Selecteer een inlog manier.", var.addonicon, 2500, False)
            return

        if newLoginTypeEmailadres == True and newLoginTypeAbonnementsnummer == True:
            xbmcgui.Dialog().notification(var.addonname, "Selecteer 1 van de 2 inlog manieren.", var.addonicon, 2500, False)
            return

        if newLoginTypeAbonnementsnummer == True and (func.string_isnullorempty(newLoginUsername) == True or func.string_isnullorempty(newLoginPassword) == True):
            xbmcgui.Dialog().notification(var.addonname, "Vul alstublieft uw inlog gegevens in.", var.addonicon, 2500, False)
            return

        if newLoginTypeEmailadres == True and (func.string_isnullorempty(newLoginEmail) == True or func.string_isnullorempty(newLoginPasswordEmail) == True):
            xbmcgui.Dialog().notification(var.addonname, "Vul alstublieft uw inlog gegevens in.", var.addonicon, 2500, False)
            return

        #Set settings
        if newLoginTypeAbonnementsnummer == True:
            getset.setting_set('LoginType', 'Abonnementsnummer')
        else:
            getset.setting_set('LoginType', 'Emailadres')
        getset.setting_set('LoginUsername', newLoginUsername)
        getset.setting_set('LoginPassword', newLoginPassword)
        getset.setting_set('LoginEmail', newLoginEmail)
        getset.setting_set('LoginPasswordEmail', newLoginPasswordEmail)
        getset.setting_set('LoginChecked', 'false')

        #Attempt to login
        if apilogin.ApiLogin(True, True) == True:
            close_welcome(True)
