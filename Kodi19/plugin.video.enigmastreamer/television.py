from datetime import datetime, timedelta
from threading import Thread
import enigma
import func
import var
import xbmc
import xbmcgui
import zap

def switch_to_page():
    if var.guiTelevision == None:
        var.guiTelevision = Gui('television.xml', var.addonpath, 'default', '720p')
        var.guiTelevision.show()

def close_the_page():
    if var.guiTelevision != None:
        #Reset the page busy status
        var.busy_television = False

        #Stop the epg refresh thread
        var.thread_refresh_epgtv = None

        #Close the shown window
        var.guiTelevision.close()
        var.guiTelevision = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Add menu buttons to the page
        self.list_add_menu()

        #Add channels to the page
        self.list_update_channels(False)

        #Start the epg update thread
        if var.thread_refresh_epgtv == None:
            var.thread_refresh_epgtv = Thread(target=self.thread_refresh_epgtv)
            var.thread_refresh_epgtv.start()

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
                elif listItemAction == 'receiver_standby': 
                    enigma.enigma_receiver_standby()
            elif clickId == 1001:
                listItemSelected = clickedControl.getSelectedItem()
                enigma.enigma_stream(listItemSelected)
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

        listitem = xbmcgui.ListItem('Refresh channels')
        listitem.setProperty('Action', 'refresh_list')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/refresh.png'),'icon': func.path_resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Receiver standby')
        listitem.setProperty('Action', 'receiver_standby')
        listitem.setArt({'thumb': func.path_resources('resources/skins/default/media/common/shutdown.png'),'icon': func.path_resources('resources/skins/default/media/common/shutdown.png')})
        listcontainer.addItem(listitem)

        #Focus on the menu buttons
        listcontainer = self.getControl(1000)
        self.setFocus(listcontainer)
        xbmc.sleep(200)

    def refresh_programs(self):
        try:
            if var.busy_television == True:
                notificationIcon = func.path_resources('resources/skins/default/media/common/refresh.png')
                xbmcgui.Dialog().notification(var.addonname, 'Already refreshing.', notificationIcon, 2500, False)
                return
            self.list_update_channels(True)
            self.list_update_epg()
        except:
            pass

    def list_update_channels(self, forceUpdate):
        if var.busy_television == True:
            notificationIcon = func.path_resources('resources/skins/default/media/common/refresh.png')
            xbmcgui.Dialog().notification(var.addonname, 'Already refreshing.', notificationIcon, 2500, False)
            return
        var.busy_television = True

        listcontainer = self.getControl(1001)

        #Check if update is needed
        if not forceUpdate:
            if listcontainer.size() > 0:
                var.busy_television = False
                return

        #Clear channels from the list
        listcontainer.reset()

        #Update the load status
        func.updateLabelText(self, 1, 'Loading channels')

        #Get channels from enigma
        try:
            list_items = enigma.enigma_list_channels(var.currentBouquet)
        except:
            func.updateLabelText(self, 1, 'Load failed')
            var.busy_television = False
            return

        #Update the load status
        func.updateLabelText(self, 1, 'Checking channels')

        #Check channels list
        if list_items == None:
            func.updateLabelText(self, 1, 'No channels')
            var.busy_television = False
            return

        #List enigma channels
        ChannelNumber = 0
        controls = list_items.findall('e2service')
        for control in controls:
            e2servicereference = control.find('e2servicereference').text
            e2servicename = control.find('e2servicename').text
            ChannelNumber += 1

            if e2servicename[0].isalpha() or e2servicename[0].isdigit():
                ChannelName = '[COLOR grey]' + str(ChannelNumber) + '[/COLOR] ' + e2servicename
                ProgramNameNow = 'Loading information'
                ProgramDescription = 'Loading program description.'
            else:
                ChannelName = '[COLOR grey]' + str(ChannelNumber) + '[/COLOR] [COLOR dimgrey]' + e2servicename + '[/COLOR]'
                ProgramNameNow = ''
                ProgramDescription = '[COLOR dimgrey]Channels subgroup:[/COLOR]\n' + e2servicename

            listitem = xbmcgui.ListItem()
            listitem.setProperty('ChannelNumber', str(ChannelNumber))
            listitem.setProperty('ChannelName', ChannelName)
            listitem.setProperty('ProgramNameNow', ProgramNameNow)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setProperty('e2servicename', e2servicename)
            listitem.setProperty('e2servicereference', e2servicereference)
            listcontainer.addItem(listitem)

        #Update the total list count
        total_items = listcontainer.size()
        func.updateLabelText(self, 1, str(total_items) + ' channels')

        #Focus on the item list
        if total_items > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(200)

    def thread_refresh_epgtv(self):
        LastTime = (datetime.now() - timedelta(minutes=1)).strftime('%H:%M')
        while var.thread_refresh_epgtv != None and var.addonmonitor.abortRequested() == False:
            CurrentTime = datetime.now().strftime('%H:%M')
            if LastTime == CurrentTime: #Check if minute passed
                xbmc.sleep(1000)
            else:
                LastTime = CurrentTime
                var.busy_television = True
                self.list_update_epg()
                var.busy_television = False

    def list_update_epg(self):
        #Get and check the list container
        listcontainer = self.getControl(1001)
        listitemcount = listcontainer.size()

        #Set the current channel id
        for channelNum in range(0, listitemcount):
            updateItem = listcontainer.getListItem(channelNum)
            ProgramNameNow = updateItem.getProperty('ProgramNameNow')
            e2servicereference = updateItem.getProperty('e2servicereference')

            if not func.string_isnullorempty(ProgramNameNow):
                #Get epg info from enigma
                try:
                    epg_data = enigma.enigma_epg_information(e2servicereference)
                except:
                    updateItem.setProperty('ProgramNameNow', 'Information not available')
                    continue

                #Check epg data
                if epg_data == None:
                    updateItem.setProperty('ProgramNameNow', 'Information not available')
                    continue

                #Get program information
                controls = epg_data.findall('e2event')
                for control in controls:
                    ProgramDurationNow = control.find('e2eventduration').text
                    ProgramStartTimeNow = control.find('e2eventstart').text
                    ProgramProgressPercent = '0'
                    ProgramProgressPercentVisible = 'false'

                    e2eventtitle = control.find('e2eventtitle').text
                    if e2eventtitle == None: e2eventtitle = 'Unknown program'

                    e2eventdescription = control.find('e2eventdescription').text
                    if e2eventdescription == None: e2eventdescription = ''

                    e2eventdescriptionextended = control.find('e2eventdescriptionextended').text
                    if e2eventdescriptionextended == None: e2eventdescriptionextended = ''

                    if not func.string_isnullorempty(e2eventdescriptionextended):
                        ProgramDescription = e2eventdescriptionextended + '\n\n'
                    else:
                        ProgramDescription = 'Full description is not available.\n\n'

                    if not func.string_isnullorempty(e2eventdescription):
                        ProgramDescription = ProgramDescription + '[COLOR grey]' + e2eventdescription + '[/COLOR]'

                    if ProgramStartTimeNow != '0' and ProgramDurationNow != '0':
                        ProgramStartTimeNow = datetime.fromtimestamp(int(ProgramStartTimeNow))
                        ProgramEndTimeNow = ProgramStartTimeNow + timedelta(seconds=int(ProgramDurationNow))
                        ProgramNameNow = '(' + ProgramStartTimeNow.strftime('%H:%M') + '/' + ProgramEndTimeNow.strftime('%H:%M') + ') '
                        ProgramProgressPercentVisible = 'true'
                        ProgramProgressPercent = str(int(((datetime.now() - ProgramStartTimeNow).total_seconds() / 60) * 100 / ((ProgramEndTimeNow - ProgramStartTimeNow).total_seconds() / 60)))

                        ProgramTimeLeftNow = str(int(((ProgramEndTimeNow - datetime.now()).total_seconds() / 60)))
                        if ProgramTimeLeftNow == '0':
                            ProgramDescription = '[COLOR gray]Almost ending, was ' + str(int(ProgramDurationNow) / 60) + ' minutes long and started around ' + ProgramStartTimeNow.strftime('%H:%M') + '[/COLOR]\n\n' + ProgramDescription
                        else:
                            ProgramDescription = '[COLOR gray]' + ProgramTimeLeftNow + ' min remaining from the ' + str(int(ProgramDurationNow) / 60) + ' minutes, started around ' + ProgramStartTimeNow.strftime('%H:%M') + ' and ends at ' + ProgramEndTimeNow.strftime('%H:%M') + '[/COLOR]\n\n' + ProgramDescription

                    ProgramNameNow += e2eventtitle
                    if 'N/A' in ProgramNameNow:
                        ProgramNameNow = 'Information not available'                        

                    updateItem.setProperty('ProgramDescription', ProgramDescription)
                    updateItem.setProperty('ProgramProgressPercent', ProgramProgressPercent)
                    updateItem.setProperty('ProgramProgressPercentVisible', ProgramProgressPercentVisible)
                    updateItem.setProperty('ProgramNameNow', ProgramNameNow)
