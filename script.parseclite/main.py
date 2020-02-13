import default
import func
import parsec
import var
import xbmc
import xbmcgui

def switch_to_page():
    if var.guiMain == None:
        var.guiMain = Gui('main.xml', var.addonpath, 'default', '720p')
        var.guiMain.doModal()
        var.guiMain = None

def close_the_page():
    if var.guiMain != None:
        #Clear used global variables
        default.clear_home_variables()

        #Close the shown window
        var.guiMain.close()

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Add menu buttons to the page
        self.list_add_menu()

        #Focus on the menu buttons
        listcontainer = self.getControl(1000)
        self.setFocus(listcontainer)
        xbmc.sleep(200)

    def list_add_menu(self):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0: return

        listitem = xbmcgui.ListItem('Connect')
        listitem.setProperty('Action', 'parsec_connect')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/play.png'),'icon': func.path_resources('resources/skins/default/media/common/play.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Login')
        listitem.setProperty('Action', 'parsec_login')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/pair.png'),'icon': func.path_resources('resources/skins/default/media/common/pair.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Install Parsec')
        listitem.setProperty('Action', 'parsec_install')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/install.png'),'icon': func.path_resources('resources/skins/default/media/common/install.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Settings')
        listitem.setProperty('Action', 'addon_settings')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/settings.png'),'icon': func.path_resources('resources/skins/default/media/common/settings.png')})
        listcontainer.addItem(listitem)

    def onAction(self, action):
        actionId = action.getId()
        if actionId == var.ACTION_PREVIOUS_MENU: close_the_page()
        elif actionId == var.ACTION_BACKSPACE: close_the_page()

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'parsec_connect':
                parsec.parsec_connect()
            elif listItemAction == 'parsec_login':
                parsec.parsec_login()
            elif listItemAction == 'parsec_install':
                parsec.parsec_install()
            elif listItemAction == 'addon_settings':
                var.addon.openSettings()
