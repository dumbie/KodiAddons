import default
import func
import moonlight
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

        #Add apps list to the page
        self.list_add_apps()

    def list_add_menu(self):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0: return

        listitem = xbmcgui.ListItem('Refresh apps')
        listitem.setProperty('Action', 'moonlight_list')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/refresh.png'),'icon': func.path_resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Pair device')
        listitem.setProperty('Action', 'moonlight_pair')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/pair.png'),'icon': func.path_resources('resources/skins/default/media/common/pair.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Install moonlight')
        listitem.setProperty('Action', 'moonlight_install')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/install.png'),'icon': func.path_resources('resources/skins/default/media/common/install.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Settings')
        listitem.setProperty('Action', 'addon_settings')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/settings.png'),'icon': func.path_resources('resources/skins/default/media/common/settings.png')})
        listcontainer.addItem(listitem)

        #Focus on the menu
        self.setFocus(listcontainer)
        xbmc.sleep(200)
        listcontainer.selectItem(0)
        xbmc.sleep(200)

    def list_add_apps(self):
        #Check if addon is busy
        if var.busy_main == True: return
        var.busy_main = True

        #Clear apps from the list
        listcontainer = self.getControl(1001)
        listcontainer.reset()

        #Update the load status
        func.updateLabelText(self, 1, 'Loading apps')

        #Get apps from moonlight
        try:
            list_apps = str(moonlight.moonlight_list())
        except:
            func.updateLabelText(self, 1, 'Load failed')
            var.busy_main = False
            return

        #Update the load status
        func.updateLabelText(self, 1, 'Checking apps')

        #Check moonlight apps
        if func.string_isnullorempty(list_apps) == True:
            func.updateLabelText(self, 1, 'No connection')
            var.busy_main = False
            return
        elif "You must pair" in list_apps:
            func.updateLabelText(self, 1, 'Not paired')
            var.busy_main = False
            return
        elif "Can't connect" in list_apps:
            func.updateLabelText(self, 1, 'Connect error')
            var.busy_main = False
            return

        #List moonlight apps
        for appName in list_apps.split('\n'):
            if func.string_isnullorempty(appName) == False and appName[0].isdigit() == True:
                appName = appName.lstrip('0123456789. ')
                listitem = xbmcgui.ListItem(appName)
                listcontainer.addItem(listitem)

        #Update the total app count
        total_apps = listcontainer.size()
        func.updateLabelText(self, 1, str(total_apps) + ' apps')

        #Focus on the apps list or menu
        if total_apps > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(200)
            listcontainer.selectItem(0)
            xbmc.sleep(200)
        else:
            listcontainer = self.getControl(1000)
            self.setFocus(listcontainer)
            xbmc.sleep(200)
            listcontainer.selectItem(0)
            xbmc.sleep(200)

        var.busy_main = False

    def onAction(self, action):
        actionId = action.getId()
        if actionId == var.ACTION_PREVIOUS_MENU: close_the_page()
        elif actionId == var.ACTION_BACKSPACE: close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'moonlight_list':
                self.list_add_apps()
            elif listItemAction == 'moonlight_pair':
                #Check if addon is busy
                if var.busy_main == True: return
                var.busy_main = True
                moonlight.moonlight_pair()
                var.busy_main = False
            elif listItemAction == 'moonlight_install':
                #Check if addon is busy
                if var.busy_main == True: return
                var.busy_main = True
                moonlight.moonlight_install()
                var.busy_main = False
            elif listItemAction == 'addon_settings':
                var.addon.openSettings()
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            moonlight.moonlight_stream(listItemSelected.getLabel())
