import default
import enigma
import func
import recordings
import television
import var
import xbmc
import xbmcgui
import zap

def switch_to_page():
    if var.guiMain == None:
        var.guiMain = Gui('main.xml', var.addonpath, 'default', '720p')
        var.guiMain.doModal()
        var.guiMain = None

def close_the_page():
    if var.guiMain != None:
        #Stop the playing media
        xbmc.Player().stop()

        #Clear used global variables
        default.clear_home_variables()

        #Close the shown window
        var.guiMain.close()

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Add menu buttons to the page
        self.list_add_menu()

        #Add bouquets list to the page
        self.list_update_bouquets(False)

    def list_add_menu(self):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0: return

        listitem = xbmcgui.ListItem('Refresh bouquets')
        listitem.setProperty('Action', 'refresh_list')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/refresh.png'),'icon': func.path_resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Show recordings')
        listitem.setProperty('Action', 'show_recordings')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/record.png'),'icon': func.path_resources('resources/skins/default/media/common/record.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Settings')
        listitem.setProperty('Action', 'addon_settings')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/settings.png'),'icon': func.path_resources('resources/skins/default/media/common/settings.png')})
        listcontainer.addItem(listitem)

        #Focus on the menu buttons
        listcontainer = self.getControl(1000)
        self.setFocus(listcontainer)
        xbmc.sleep(200)

    def list_update_bouquets(self, forceUpdate):
        if var.busy_main == True:
            notificationIcon = func.path_resources('resources/skins/default/media/common/refresh.png')
            xbmcgui.Dialog().notification(var.addonname, 'Already refreshing.', notificationIcon, 2500, False)
            return
        var.busy_main = True

        listcontainer = self.getControl(1001)

        #Check if update is needed
        if not forceUpdate:
            if listcontainer.size() > 0:
                var.busy_main = False
                return

        #Clear channels from the list
        listcontainer.reset()

        #Update the load status
        func.updateLabelText(self, 1, 'Loading bouquets')

        #Get bougets from enigma
        try:
            list_items = enigma.enigma_list_bouquets()
        except:
            func.updateLabelText(self, 1, 'Load failed')
            var.busy_main = False
            return

        #Update the load status
        func.updateLabelText(self, 1, 'Checking bouquets')

        #Check bouquets list
        if list_items == None:
            func.updateLabelText(self, 1, 'No bouquets')
            var.busy_main = False
            return

        #List enigma bouquets
        ChannelNumber = 0
        controls = list_items.findall('e2service')
        for control in controls:
            e2servicereference = control.find('e2servicereference').text
            e2servicename = control.find('e2servicename').text

            ChannelNumber += 1
            ChannelName = '[COLOR grey]' + str(ChannelNumber) + '[/COLOR] ' + e2servicename

            listitem = xbmcgui.ListItem(ChannelName)
            listitem.setProperty('ChannelNumber', str(ChannelNumber))
            listitem.setProperty('e2servicereference', e2servicereference)
            listitem.setProperty('e2servicename', e2servicename)
            listcontainer.addItem(listitem)

        #Update the total list count
        total_items = listcontainer.size()
        func.updateLabelText(self, 1, str(total_items) + ' bouquets')

        #Focus on the item list
        if total_items > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(200)

        var.busy_main = False

    def onClick(self, clickId):
        if var.thread_zap_wait_timer == None:
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'refresh_list':
                    self.list_update_bouquets(True)
                if listItemAction == 'show_recordings':
                    recordings.switch_to_page()
                elif listItemAction == 'addon_settings':
                    var.addon.openSettings()
            elif clickId == 1001:
                listItemSelected = clickedControl.getSelectedItem()
                var.currentBouquet = listItemSelected.getProperty('e2servicereference')
                television.switch_to_page()
            elif clickId == 3000:
                xbmc.executebuiltin('Action(FullScreen)')
            elif clickId == 3001:
                close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        if actionId == var.ACTION_PREVIOUS_MENU: close_the_page()
        elif actionId == var.ACTION_BACKSPACE: close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')
        else: zap.check_remote_number(self, 1001, actionId, True, False)
