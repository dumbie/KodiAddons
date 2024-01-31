from datetime import datetime, timedelta
import xbmc
import xbmcgui
import alarm
import lichanneltelevision
import dialog
import download
import func
import lifunc
import metadatafunc
import path
import recordingfunc
import searchdialog
import streamplay
import liepgload
import liepgupdate
import var
import zap

def switch_to_page():
    if var.guiEpg == None:
        var.guiEpg = Gui('epg.xml', var.addonpath, 'default', '720p')
        var.guiEpg.show()

def close_the_page():
    if var.guiEpg != None:
        #Stop update progress threads
        var.thread_update_epg_program.Stop()
        var.thread_update_epg_channel.Stop()

        #Close the shown window
        var.guiEpg.close()
        var.guiEpg = None

class Gui(xbmcgui.WindowXML):
    ProgramPauseUpdate = False
    ProgramManualUpdate = False
    ChannelPauseUpdate = False
    ChannelManualUpdate = False

    def onInit(self):
        self.buttons_add_navigation()
        self.load_recording_event(False)
        self.load_recording_series(False)
        channelsLoaded = self.load_channels()
        if channelsLoaded == True:
            self.set_channel_epg_variables()
            self.load_programs()
            self.start_threads()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer.Finished():
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'go_back':
                    close_the_page()
                elif listItemAction == 'set_load_day':
                    self.dialog_set_day()
                elif listItemAction == "search_channel":
                    self.search_channel()
                elif listItemAction == "search_program":
                    self.search_program()
                elif listItemAction == "switch_all_favorites":
                    self.switch_all_favorites()
                elif listItemAction == "refresh_epg":
                    self.load_programs(True)
            elif clickId == 1001:
                self.set_channel_epg_variables()
                self.load_programs(False, True)
            elif clickId == 1002:
                self.open_context_menu(clickedControl)
            elif clickId == 9000:
                if xbmc.Player().isPlayingVideo():
                    var.PlayerCustom.Fullscreen(True)
                else:
                    listContainer = self.getControl(1000)
                    self.setFocus(listContainer)
                    xbmc.sleep(100)
            elif clickId == 9001:
                self.focus_on_item_list()
            elif clickId == 3001:
                close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            listContainer.selectItem(listContainer.getSelectedPosition() + 1)
            xbmc.sleep(100)
            self.set_channel_epg_variables()
            self.load_programs()
        elif actionId == var.ACTION_PREV_ITEM:
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            listContainer.selectItem(listContainer.getSelectedPosition() - 1)
            xbmc.sleep(100)
            self.set_channel_epg_variables()
            self.load_programs()
        elif actionId == var.ACTION_PLAYER_PLAY:
            self.dialog_set_day()
        elif actionId == var.ACTION_PLAYER_FORWARD:
            self.dialog_set_day()
        elif actionId == var.ACTION_PLAYER_REWIND:
            self.dialog_set_day()
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_program()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM):
            focusedProgram = xbmc.getCondVisibility('Control.HasFocus(1002)')
            if focusedProgram:
                clickedControl = self.getControl(1002)
                self.open_context_menu(clickedControl)
        else:
            zap.check_remote_number(self, 1001, actionId, True, True)

    def start_threads(self):
        #Force manual epg update
        self.ProgramManualUpdate = True
        self.ChannelManualUpdate = True

        #Start update progress threads
        var.thread_update_epg_program.Start(self.thread_update_program_progress)
        var.thread_update_epg_channel.Start(self.thread_update_channel_progress)

    def buttons_add_navigation(self):
        listContainer = self.getControl(1000)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga een stap terug')
        listItem.setProperty('Action', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'),'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek naar zender')
        listItem.setProperty('Action', 'search_channel')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek programma')
        listItem.setProperty('Action', 'search_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Selecteer dag')
        listItem.setProperty('Action', 'set_load_day')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/calendar.png'),'icon': path.resources('resources/skins/default/media/common/calendar.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Alle of favorieten')
        listItem.setProperty('Action', 'switch_all_favorites')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/star.png'), 'icon': path.resources('resources/skins/default/media/common/star.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Vernieuwen')
        listItem.setProperty('Action', 'refresh_epg')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listContainer.addItem(listItem)

    def focus_on_channel_list(self, forceFocus=False):
        if var.EpgCurrentChannelId == '':
            selectChannelId = var.addon.getSetting('CurrentChannelId')
        else:
            selectChannelId = var.EpgCurrentChannelId
        lifunc.focus_on_channelid_in_list(self, 1001, 0, forceFocus, selectChannelId)

    def focus_on_item_list(self):
        #Get and check channel list container
        listContainer = self.getControl(1001)
        if listContainer.size() > 0:
            self.setFocus(listContainer)
            xbmc.sleep(100)
            return

        #Get and check program list container
        listContainer = self.getControl(1002)
        if listContainer.size() > 0:
            self.setFocus(listContainer)
            xbmc.sleep(100)
            return

    def dialog_set_day(self):
        #Set dates to array
        dialogAnswers = []

        for x in range(var.VodDayOffsetPast + var.EpgDaysOffsetFuture):
            dayString = func.day_string_from_day_offset(x - var.VodDayOffsetPast)
            dialogAnswers.append(dayString)

        dialogHeader = 'Selecteer dag'
        dialogSummary = 'Selecteer de gewenste televisie gids dag.'
        dialogFooter = ''

        #Get day selection index
        selectIndex = var.VodDayOffsetPast + -func.day_offset_from_datetime(var.EpgCurrentLoadDateTime)

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers, selectIndex)
        if dialogResult == 'DialogCancel':
            return

        #Calculate selected day offset
        selectedIndex = (dialogAnswers.index(dialogResult) - var.VodDayOffsetPast)

        #Update selected day loading time
        var.EpgCurrentLoadDateTime = func.datetime_from_day_offset(selectedIndex)

        #Load the channel epg
        self.load_programs()

    def open_context_menu(self, clickedControl):
        listItemSelected = clickedControl.getSelectedItem()
        ProgramTimeStartString = listItemSelected.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartString, '%Y-%m-%d %H:%M:%S')
        ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
        ProgramTimeEndString = listItemSelected.getProperty('ProgramTimeEnd')
        ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndString, '%Y-%m-%d %H:%M:%S')
        ProgramName = listItemSelected.getProperty('ProgramName')
        ChannelName = listItemSelected.getProperty('ChannelName')

        #Check if current program is airing and user has recording access
        dateTimeNow = datetime.now()
        if var.RecordingAccess() == True:
            if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
                dialogAnswers = ['Live programma kijken', 'Programma opnemen of annuleren', 'Serie seizoen opnemen of annuleren']
                dialogHeader = 'Programma kijken of opnemen'
                dialogSummary = ProgramName + ' kijken of opnemen?'
                dialogFooter = ''
            elif ProgramTimeStartDateTime < dateTimeNow:
                dialogAnswers = ['Programma terug kijken', 'Serie seizoen opnemen of annuleren']
                dialogHeader = 'Programma terug kijken of opnemen'
                dialogSummary = ProgramName + ' terug kijken of opnemen?'
                dialogFooter = ''
            else:
                dialogAnswers = ['Alarm zetten of annuleren', 'Programma opnemen of annuleren', 'Serie seizoen opnemen of annuleren']
                dialogHeader = 'Alarm zetten of opnemen'
                dialogSummary = ProgramName + ' alarm zetten of opnemen?'
                dialogFooter = ''
        else:
            if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
                dialogAnswers = ['Live programma kijken']
                dialogHeader = 'Programma kijken'
                dialogSummary = ProgramName + ' op ' + ChannelName + ' kijken?'
                dialogFooter = ''
            elif ProgramTimeStartDateTime < dateTimeNow:
                dialogAnswers = ['Programma terug kijken']
                dialogHeader = 'Programma terug kijken'
                dialogSummary = ProgramName + ' terug kijken?'
                dialogFooter = ''
            else:
                dialogAnswers = ['Alarm zetten of annuleren']
                dialogHeader = 'Alarm zetten'
                dialogSummary = ProgramName + ' alarm zetten?'
                dialogFooter = ''

        #Add switch favorite/all button
        if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
            dialogAnswers.append('Toon alle zenders')
        else:
            dialogAnswers.append('Toon favorieten zenders')

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Alarm zetten of annuleren':
            self.set_program_alarm(listItemSelected)
        elif dialogResult == 'Programma opnemen of annuleren':
            recordingfunc.record_event_epg(self, listItemSelected)
        elif dialogResult == 'Serie seizoen opnemen of annuleren':
            recordingfunc.record_series_epg(self, listItemSelected)
        elif dialogResult == 'Live programma kijken':
            streamplay.play_tv(listItemSelected)
        elif dialogResult == 'Programma terug kijken':
            streamplay.play_program(listItemSelected, False)
        elif dialogResult == 'Toon alle zenders' or dialogResult == 'Toon favorieten zenders':
            self.switch_all_favorites()

    def switch_all_favorites(self):
        try:
            #Switch favorites mode on or off
            if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
                var.addon.setSetting('LoadChannelFavoritesOnly', 'false')
            else:
                #Check if there are favorites set
                if var.FavoriteTelevisionJson == []:
                    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
                    xbmcgui.Dialog().notification(var.addonname, 'Geen favorieten zenders.', notificationIcon, 2500, False)
                    return
                var.addon.setSetting('LoadChannelFavoritesOnly', 'true')

            channelsLoaded = self.load_channels(True)
            if channelsLoaded == True:
                self.set_channel_epg_variables()
                self.load_programs(False, True)
        except:
            pass

    def update_channel_status(self):
        #Clear expired alarms from Json
        alarm.alarm_clean_expired()

        #Get and check the list container
        listContainer = self.getControl(1001)
        listItemCount = listContainer.size()

        #Update all channel status icons
        for itemNum in range(0, listItemCount):
            try:
                #Check if epg is allowed to update
                if self.ChannelPauseUpdate: return

                updateItem = listContainer.getListItem(itemNum)
                liepgupdate.list_update_channel(updateItem)
            except:
                pass

    def update_program_status(self):
        #Get and check the list container
        listContainer = self.getControl(1002)
        listItemCount = listContainer.size()

        #Update all program progress and status
        for itemNum in range(0, listItemCount):
            try:
                #Check if epg is allowed to update
                if self.ProgramPauseUpdate: return

                updateItem = listContainer.getListItem(itemNum)
                liepgupdate.list_update_program(updateItem)
            except:
                pass

    def set_program_alarm(self, listItemSelected):
        ProgramTimeStartString = listItemSelected.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartString, '%Y-%m-%d %H:%M:%S')
        ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)

        ChannelId = listItemSelected.getProperty('ChannelId')
        ExternalId = listItemSelected.getProperty('ExternalId')
        ChannelName = listItemSelected.getProperty('ChannelName')
        ProgramName = listItemSelected.getProperty('ProgramName')

        alarmAdded = alarm.alarm_add(ProgramTimeStartDateTime, ChannelId, ExternalId, ChannelName, ProgramName, True)
        #Update alarm icon in the channel and epg list
        if alarmAdded == True:
            #Force manual epg update
            self.ProgramManualUpdate = True
            self.ChannelManualUpdate = True
        elif alarmAdded == 'Remove':
            #Force manual epg update
            self.ProgramManualUpdate = True
            self.ChannelManualUpdate = True

    def search_channel(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistoryChannel.js', 'Zoek naar zender')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchChannelTerm = func.search_filter_string(searchDialogTerm.string)
        channelsLoaded = self.load_channels(True)
        var.SearchChannelTerm = ''
        if channelsLoaded == True:
            self.set_channel_epg_variables()
            self.load_programs(False, True)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek programma')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchChannelTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_programs(False, True, True)
        var.SearchChannelTerm = ''

    def set_channel_epg_variables(self):
        #Set the currently selected channel
        listContainer = self.getControl(1001)
        listItemSelected = listContainer.getSelectedItem()
        if listItemSelected == None:
            func.updateLabelText(self, 1, 'Selecteer zender')
            func.updateLabelText(self, 2, "[COLOR gray]Selecteer de gewenste televisie zender.[/COLOR]")
            return

        var.EpgCurrentChannelId = listItemSelected.getProperty('ChannelId')
        var.EpgCurrentChannelName = listItemSelected.getProperty('ChannelName')

    def load_channels(self, forceLoad=False):
        self.ChannelPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        loadResult = self.load_channels_code(forceLoad)
        self.ChannelPauseUpdate = False
        return loadResult

    def load_channels_code(self, forceLoad=False):
        #Get and check the list container
        listContainer = self.getControl(1001)
        if forceLoad == False:
            if listContainer.size() > 0:
                self.focus_on_channel_list(False)
                return True
        else:
            listContainer.reset()

        #Download the channels
        func.updateLabelText(self, 1, 'Zenders downloaden')
        func.updateLabelText(self, 2, '[COLOR gray]Zenders worden gedownload, nog even geduld...[/COLOR]')
        downloadResult = download.download_channels_tv(False)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            func.updateLabelText(self, 2, '[COLOR gray]TV Gids is niet beschikbaar.[/COLOR]')
            listContainer = self.getControl(1000)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            listContainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, 'Zenders laden')
        func.updateLabelText(self, 2, '[COLOR gray]Zenders worden geladen, nog even geduld...[/COLOR]')

        #Add items to sort list
        listContainerSort = []
        lichanneltelevision.list_load(listContainerSort)

        #Sort and add items to container
        listContainer.addItems(listContainerSort)

        #Focus on the list container
        if listContainer.size() > 0:
            self.focus_on_channel_list(True)
        else:
            #Set channel type string
            channelTypeString = 'zenders'
            if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
                channelTypeString = 'favorieten zenders'

            #Update status label text
            listContainer = self.getControl(1000)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                func.updateLabelText(self, 2, "[COLOR gray]Zender[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]niet gevonden.[/COLOR]")
                listContainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen ' + channelTypeString)
                func.updateLabelText(self, 2, "[COLOR gray]Geen beschikbare " + channelTypeString + ".[/COLOR]")
                listContainer.selectItem(0)
            xbmc.sleep(100)

            #Focus on channel list
            self.setFocus(listContainer)
            xbmc.sleep(100)

            #Reset the program list
            listContainer = self.getControl(1002)
            listContainer.reset()
            return False

        #Force manual epg update
        self.ChannelManualUpdate = True

        return True

    def load_recording_event(self, forceUpdate=False):
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False: return False

    def load_recording_series(self, forceUpdate=False):
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False: return False

    def load_programs(self, forceUpdate=False, forceLoad=False, forceFocus=False):
        self.ProgramPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.load_programs_code(forceUpdate, forceLoad, forceFocus)
        self.ProgramPauseUpdate = False

    def load_programs_code(self, forceUpdate=False, forceLoad=False, forceFocus=False):
        #Get and check the list container
        listContainer = self.getControl(1002)
        listItemCount = listContainer.size()

        #Check if channel has changed
        epgChannelChanged = var.EpgPreviousChannelId != var.EpgCurrentChannelId

        #Check epg day has changed
        epgDayTimeChanged = var.EpgPreviousLoadDateTime != var.EpgCurrentLoadDateTime

        #Check if update is needed
        if forceLoad or forceUpdate or epgChannelChanged or epgDayTimeChanged or listItemCount == 0:
            #Clear the current epg items
            listContainer.reset()

            #Download the epg day information
            func.updateLabelText(self, 1, 'Gids download')
            func.updateLabelText(self, 2, '[COLOR gray]TV Gids wordt gedownload, nog even geduld...[/COLOR]')
            var.EpgCurrentDayDataJson = download.download_epg_day(var.EpgCurrentLoadDateTime, forceUpdate)
            if var.EpgCurrentDayDataJson == None:
                func.updateLabelText(self, 1, 'Niet beschikbaar')
                func.updateLabelText(self, 2, '[COLOR gray]TV Gids is niet beschikbaar.[/COLOR]')
                listContainer = self.getControl(1000)
                self.setFocus(listContainer)
                xbmc.sleep(100)
                listContainer.selectItem(0)
                xbmc.sleep(100)
                return
        else:
            return

        #Update epg status
        func.updateLabelText(self, 1, 'Gids laden')
        func.updateLabelText(self, 2, '[COLOR gray]TV Gids wordt geladen, nog even geduld...[/COLOR]')

        listContainerSort = []
        if func.string_isnullorempty(var.SearchChannelTerm):
            #Load programs for set day and channel
            channelEpgJson = metadatafunc.search_channelid_jsonepg(var.EpgCurrentDayDataJson, var.EpgCurrentChannelId)
            if channelEpgJson == None:
                func.updateLabelText(self, 1, 'Zender gids mist')
                func.updateLabelText(self, 2, '[COLOR gray]TV Gids is niet beschikbaar voor[/COLOR] ' + var.EpgCurrentChannelName)
                return

            #Add items to sort list
            liepgload.list_load(listContainerSort, channelEpgJson)
        else:
            #Load programs for search term from all channels
            for channelEpgJson in var.EpgCurrentDayDataJson["resultObj"]["containers"]:
                #Add items to sort list
                liepgload.list_load(listContainerSort, channelEpgJson)

        #Sort and add items to container
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramTimeStart'))
        listContainer.addItems(listContainerSort)

        #Select program index
        self.epg_selectindex_program(forceFocus)

        #Update the status
        self.count_epg(var.EpgCurrentChannelName)

        #Force manual epg update
        self.ProgramManualUpdate = True

        #Update epg variables
        var.EpgPreviousChannelId = var.EpgCurrentChannelId
        var.EpgPreviousLoadDateTime = var.EpgCurrentLoadDateTime

    #Epg program select index
    def epg_selectindex_program(self, forceFocus=False):
        #Get and check the list container
        listContainer = self.getControl(1002)
        listItemCount = listContainer.size()

        #Check program list item count
        if listItemCount == 0: return

        programSelectIndexAiring = 0
        programSelectIndexUpcoming = 0
        programSelectIndexNavigate = 0

        #Check if program is airing or matches navigate index
        for itemNum in range(0, listItemCount):
            listItem = listContainer.getListItem(itemNum)

            #Check if program matches navigate id
            if var.EpgNavigateProgramId == listItem.getProperty('ProgramId'):
                programSelectIndexNavigate = itemNum
                break

            #Check if program is still to come
            if programSelectIndexUpcoming == 0 and listItem.getProperty('ProgramIsUpcoming') == 'true':
                programSelectIndexUpcoming = itemNum

            #Check if program is currently airing
            if listItem.getProperty('ProgramIsAiring') == 'true':
                programSelectIndexAiring = itemNum

        #Select program list item
        if programSelectIndexNavigate != 0:
            forceFocus = True
            listContainer.selectItem(programSelectIndexNavigate)
        elif programSelectIndexAiring != 0:
            listContainer.selectItem(programSelectIndexAiring)
        elif programSelectIndexUpcoming != 0:
            listContainer.selectItem(programSelectIndexUpcoming)
        else:
            listContainer.selectItem(0)
        xbmc.sleep(100)

        #Focus on program list
        if forceFocus:
            self.setFocus(listContainer)
            xbmc.sleep(100)

        #Reset navigate variable
        var.EpgNavigateProgramId = ''

    #Update the status
    def count_epg(self, ChannelName):
        #Set loading day string
        loadDayString = func.day_string_from_datetime(var.EpgCurrentLoadDateTime)

        #Update the label texts
        listContainer = self.getControl(1002)
        if listContainer.size() == 0:
            if var.SearchChannelTerm == '':
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 2, "[COLOR gray]Geen programma's beschikbaar voor[/COLOR] " + ChannelName + " [COLOR gray]op[/COLOR] " + loadDayString)
            else:
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 2, "[COLOR gray]Programma[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]niet gevonden op[/COLOR] " + loadDayString)
        else:
            if var.SearchChannelTerm == '':
                func.updateLabelText(self, 1, str(listContainer.size()) + " programma's")
                func.updateLabelText(self, 2, "[COLOR gray]Alle programma's voor[/COLOR] " + ChannelName + " [COLOR gray]op[/COLOR] " + loadDayString)
            else:
                func.updateLabelText(self, 1, str(listContainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 2, "[COLOR gray]Programma's gevonden voor[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]op[/COLOR] " + loadDayString)

    def thread_update_program_progress(self):
        threadLastTime = ''
        while var.thread_update_epg_program.Allowed():
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime or self.ProgramManualUpdate:
                threadLastTime = threadCurrentTime
                self.ProgramManualUpdate = False

                #Update program status
                self.update_program_status()
            else:
                var.thread_update_epg_program.Sleep(1000)

    def thread_update_channel_progress(self):
        threadLastTime = ''
        while var.thread_update_epg_channel.Allowed():
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime or self.ChannelManualUpdate:
                threadLastTime = threadCurrentTime
                self.ChannelManualUpdate = False

                #Update channel status
                self.update_channel_status()
            else:
                var.thread_update_epg_channel.Sleep(1000)
