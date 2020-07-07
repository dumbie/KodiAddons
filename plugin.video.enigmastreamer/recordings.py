import time
from datetime import datetime, timedelta
from threading import Thread
import enigma
import func
import hybrid
import var
import xbmc
import xbmcgui
import zap

def switch_to_page():
    if var.guiRecordings == None:
        var.guiRecordings = Gui('television.xml', var.addonpath, 'default', '720p')
        var.guiRecordings.show()

def close_the_page():
    if var.guiRecordings != None:
        #Reset the page busy status
        var.busy_recordings = False

        #Close the shown window
        var.guiRecordings.close()
        var.guiRecordings = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Add menu buttons to the page
        self.list_add_menu()

        #Add recordings to the page
        self.list_update_recordings(False)

    def onClick(self, clickId):
        if var.thread_zap_wait_timer == None:
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'go_back':
                    close_the_page()
                elif listItemAction == 'refresh_list':
                    self.refresh_programs()
            elif clickId == 1001:
                listItemSelected = clickedControl.getSelectedItem()
                enigma.enigma_stream_recording(listItemSelected)
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

    def list_add_menu(self):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0: return

        listitem = xbmcgui.ListItem('Go back')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/back.png'),'icon': func.path_resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Refresh recordings')
        listitem.setProperty('Action', 'refresh_list')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/refresh.png'),'icon': func.path_resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

        #Focus on the menu buttons
        listcontainer = self.getControl(1000)
        self.setFocus(listcontainer)
        xbmc.sleep(200)

    def refresh_programs(self):
        try:
            if var.busy_recordings == True:
                notificationIcon = func.path_resources('resources/skins/default/media/common/refresh.png')
                xbmcgui.Dialog().notification(var.addonname, 'Already refreshing.', notificationIcon, 2500, False)
                return
            self.list_update_recordings(True)
        except:
            pass

    def list_update_recordings(self, forceUpdate):
        if var.busy_recordings == True:
            notificationIcon = func.path_resources('resources/skins/default/media/common/refresh.png')
            xbmcgui.Dialog().notification(var.addonname, 'Already refreshing.', notificationIcon, 2500, False)
            return
        var.busy_recordings = True

        listcontainer = self.getControl(1001)

        #Check if update is needed
        if not forceUpdate:
            if listcontainer.size() > 0:
                var.busy_recordings = False
                return

        #Clear recordings from the list
        listcontainer.reset()

        #Update the load status
        func.updateLabelText(self, 1, 'Loading recordings')

        #Get recordings from enigma
        try:
            list_items = enigma.enigma_list_recordings()
        except:
            func.updateLabelText(self, 1, 'Load failed')
            var.busy_recordings = False
            return

        #Update the load status
        func.updateLabelText(self, 1, 'Checking recordings')

        #Check recordings list
        if list_items == None:
            func.updateLabelText(self, 1, 'No recordings')
            var.busy_recordings = False
            return

        #List enigma recordings
        ChannelNumber = 0
        controls = list_items.findall('e2movie')
        for control in controls:
            e2title = control.find('e2title').text
            e2title = hybrid.urllib_unquote(e2title)
            e2filename = control.find('e2filename').text
            e2filename = hybrid.urllib_quote(e2filename)

            e2servicename = control.find('e2servicename').text
            if func.string_isnullorempty(e2servicename):
                e2servicename = 'Unknown'

            e2description = control.find('e2description').text
            if func.string_isnullorempty(e2description):
                e2description = 'Unknown'

            e2descriptionextended = control.find('e2descriptionextended').text
            if func.string_isnullorempty(e2descriptionextended):
                e2descriptionextended = 'Unknown'

            e2time = int(control.find('e2time').text)
            e2length = control.find('e2length').text + 'min'

            ChannelNumber += 1
            ChannelName = '[COLOR grey]' + str(ChannelNumber) + '[/COLOR] ' + e2title

            #Get the recording time
            ProgramRecordedDateTime = time.localtime(e2time)
            ProgramRecordedDate = time.strftime("%a %d %b %Y", ProgramRecordedDateTime)
            ProgramRecordedTime = time.strftime("%H:%M", ProgramRecordedDateTime)
            ProgramRecordedString = e2servicename + ' on ' + ProgramRecordedDate + ' at ' + ProgramRecordedTime + ' duration ' + e2length

            #Set the recording description
            ProgramDescription = '[COLOR dimgrey]' + ProgramRecordedString + '[/COLOR]\n\n' + e2descriptionextended + '\n\n[COLOR dimgrey]' + e2description + '[/COLOR]'

            listitem = xbmcgui.ListItem()
            listitem.setProperty('ChannelNumber', str(ChannelNumber))
            listitem.setProperty('ChannelName', ChannelName)
            listitem.setProperty('ProgramNameNow', ProgramRecordedString)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setProperty('e2title', e2title)
            listitem.setProperty('e2filename', e2filename)
            listitem.setInfo('video', {'Genre': 'Recording'})
            listcontainer.addItem(listitem)

        #Update the total list count
        total_items = listcontainer.size()
        func.updateLabelText(self, 1, str(total_items) + ' recordings')

        #Focus on the item list
        if total_items > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(200)

        var.busy_recordings = False
