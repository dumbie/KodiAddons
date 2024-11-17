from datetime import datetime, timedelta
import xbmc
import xbmcgui
import alarmfunc
import dialog
import favoritefunc
import func
import getset
import guifunc
import lichanneltelevision
import liepgload
import liepgupdate
import lifunc
import path
import player
import recordingfunc
import search
import searchdialog
import streamplay
import var
import zap

def switch_to_page():
    if var.guiEpg == None:
        var.guiEpg = Gui('epg.xml', var.addonpath, 'default', '720p')
        var.guiEpg.setProperty('WebbiePlayerPage', 'Open')
        var.guiEpg.show()

def close_the_page():
    if var.guiEpg != None:
        #Stop update progress threads
        var.thread_update_epg_program.Stop()
        var.thread_update_epg_channel.Stop()

        #Save select index
        var.guiEpg.save_select_index()

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
        self.check_channel_epg_variables()
        channelsLoaded = self.load_channels(False)
        if channelsLoaded == True:
            self.load_programs(False)
            self.start_threads()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer.Finished():
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('ItemAction')
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
            elif clickId == 1001:
                self.load_programs(True)
            elif clickId == 1002:
                self.open_context_menu(clickedControl)
            elif clickId == 9000:
                if xbmc.Player().isPlaying():
                    player.Fullscreen(True)
                else:
                    listContainer = self.getControl(1000)
                    guifunc.controlFocus(self, listContainer)
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
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectIndex(listContainer, listContainer.getSelectedPosition() + 1)
            self.load_programs(False)
        elif actionId == var.ACTION_PREV_ITEM:
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectIndex(listContainer, listContainer.getSelectedPosition() - 1)
            self.load_programs(False)
        elif actionId == var.ACTION_PLAYER_PLAY:
            self.switch_all_favorites()
        elif actionId == var.ACTION_PAUSE:
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
        listItem.setProperty('ItemAction', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'),'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek naar zender')
        listItem.setProperty('ItemAction', 'search_channel')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek programma')
        listItem.setProperty('ItemAction', 'search_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Selecteer dag')
        listItem.setProperty('ItemAction', 'set_load_day')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/calendar.png'),'icon': path.resources('resources/skins/default/media/common/calendar.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Alle of favorieten')
        listItem.setProperty('ItemAction', 'switch_all_favorites')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/star.png'), 'icon': path.resources('resources/skins/default/media/common/star.png')})
        listContainer.addItem(listItem)

    def check_channel_epg_variables(self):
        if func.string_isnullorempty(var.EpgCurrentChannelId) == True:
            var.EpgCurrentChannelId = getset.setting_get('CurrentChannelId', True)

    def focus_on_item_list(self):
        #Get and check channel list container
        listContainer = self.getControl(1001)
        if listContainer.size() > 0:
            guifunc.controlFocus(self, listContainer)
            return

        #Get and check program list container
        listContainer = self.getControl(1002)
        if listContainer.size() > 0:
            guifunc.controlFocus(self, listContainer)
            return

    def dialog_set_day(self):
        #Set dates to array
        dialogAnswers = []

        for x in range(var.VodDayOffsetPast + var.EpgDaysOffsetFuture):
            dayString = func.day_string_from_day_offset(var.EpgDaysOffsetFuture - x)
            dialogAnswers.append(dayString)

        dialogHeader = 'Selecteer dag'
        dialogSummary = 'Selecteer de gewenste televisie gids dag.'
        dialogFooter = ''

        #Get day selection index
        currentIndex = var.EpgDaysOffsetFuture + func.day_offset_from_datetime(var.EpgCurrentLoadDateTime)

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers, currentIndex)
        if dialogResult == 'DialogCancel':
            return

        #Calculate selected day offset
        selectedIndex = var.EpgDaysOffsetFuture - dialogAnswers.index(dialogResult)

        #Update selected day loading time
        var.EpgCurrentLoadDateTime = func.datetime_from_day_offset(selectedIndex)

        #Load the channel epg
        self.load_programs(False)

    def save_select_index(self):
        try:
            listContainer = self.getControl(1002)
            listItemSelected = listContainer.getSelectedItem()
            var.EpgSelectIdentifier = listItemSelected.getProperty("ProgramId")
        except:
            pass

    def open_context_menu(self, clickedControl):
        listItemSelected = clickedControl.getSelectedItem()
        ProgramTimeStartString = listItemSelected.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartString, '%Y-%m-%d %H:%M:%S')
        ProgramTimeEndString = listItemSelected.getProperty('ProgramTimeEnd')
        ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndString, '%Y-%m-%d %H:%M:%S')

        #Check if current program is airing and user has recording access
        dateTimeNow = datetime.now()
        if var.RecordingAccess() == True:
            if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
                dialogAnswers = ['Programma live kijken', 'Programma vanaf begin kijken', 'Programma uitzendingen terugzoeken', 'Programma opnemen of annuleren', 'Serie seizoen opnemen of annuleren']
                dialogHeader = 'Programma Menu'
                dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
                dialogFooter = ''
            elif ProgramTimeStartDateTime < dateTimeNow:
                dialogAnswers = ['Programma uitzending terugkijken', 'Programma uitzendingen terugzoeken', 'Serie seizoen opnemen of annuleren']
                dialogHeader = 'Programma Menu'
                dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
                dialogFooter = ''
            else:
                dialogAnswers = ['Programma alarm zetten of annuleren', 'Programma uitzendingen terugzoeken', 'Programma opnemen of annuleren', 'Serie seizoen opnemen of annuleren']
                dialogHeader = 'Programma Menu'
                dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
                dialogFooter = ''
        else:
            if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
                dialogAnswers = ['Programma live kijken', 'Programma vanaf begin kijken', 'Programma uitzendingen terugzoeken']
                dialogHeader = 'Programma Menu'
                dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
                dialogFooter = ''
            elif ProgramTimeStartDateTime < dateTimeNow:
                dialogAnswers = ['Programma uitzending terugkijken', 'Programma uitzendingen terugzoeken']
                dialogHeader = 'Programma Menu'
                dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
                dialogFooter = ''
            else:
                dialogAnswers = ['Programma alarm zetten of annuleren', 'Programma uitzendingen terugzoeken']
                dialogHeader = 'Programma Menu'
                dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
                dialogFooter = ''

        #Add switch favorite/all button
        if getset.setting_get('LoadChannelFavoritesOnly') == 'true':
            dialogAnswers.append('Toon alle zenders')
        else:
            dialogAnswers.append('Toon favorieten zenders')

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma alarm zetten of annuleren':
            self.program_alarm_set(listItemSelected)
        elif dialogResult == 'Programma opnemen of annuleren':
            recordingfunc.record_event_epg(self, listItemSelected)
        elif dialogResult == 'Serie seizoen opnemen of annuleren':
            recordingfunc.record_series_epg(self, listItemSelected)
        elif dialogResult == 'Programma live kijken':
            streamplay.play_tv(listItemSelected)
        elif dialogResult == 'Programma vanaf begin kijken':
            self.program_watch_beginning(listItemSelected)
        elif dialogResult == 'Programma uitzending terugkijken':
            streamplay.play_program(listItemSelected)
        elif dialogResult == 'Programma uitzendingen terugzoeken':
            self.search_program_history(listItemSelected)
        elif dialogResult == 'Toon alle zenders' or dialogResult == 'Toon favorieten zenders':
            self.switch_all_favorites()

    def program_watch_beginning(self, listItemSelected):
        ProgramTimeStartString = listItemSelected.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartString, '%Y-%m-%d %H:%M:%S')
        SeekOffsetSecEnd = int((datetime.now() - ProgramTimeStartDateTime).total_seconds())
        streamplay.play_tv(listItemSelected, SeekOffsetSecEnd=SeekOffsetSecEnd)

    def switch_all_favorites(self):
        try:
            #Switch favorites mode on or off
            if favoritefunc.favorite_switch_mode() == False:
                return

            #Load channels and programs
            channelsLoaded = self.load_channels(True)
            if channelsLoaded == True:
                self.load_programs(True)
        except:
            pass

    def update_channel_status(self):
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

    def program_alarm_set(self, listItemSelected):
        ProgramTimeStartString = listItemSelected.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartString, '%Y-%m-%d %H:%M:%S')

        ChannelId = listItemSelected.getProperty('ChannelId')
        ExternalId = listItemSelected.getProperty('ExternalId')
        ChannelName = listItemSelected.getProperty('ChannelName')
        ProgramName = listItemSelected.getProperty('ProgramName')

        #Set or remove the program alarm
        alarmAdded = alarmfunc.alarm_add(ProgramTimeStartDateTime, ChannelId, ExternalId, ChannelName, ProgramName, True)

        #Update alarm icon in the information
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
        var.SearchTermResult = func.search_filter_string(searchDialogTerm.string)
        channelsLoaded = self.load_channels(True)
        var.SearchTermResult = ''
        if channelsLoaded == True:
            self.load_programs(True)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek programma')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchTermResult = func.search_filter_string(searchDialogTerm.string)
        self.load_programs(True, True)
        var.SearchTermResult = ''

    def search_program_history(self, listItemSelected):
        ProgramName = listItemSelected.getProperty("ProgramName")
        close_the_page()
        search.search_update_term(ProgramName)
        search.switch_to_page()

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
                lifunc.focus_listcontainer_value(self, 1001, 0, False, 'ChannelId', var.EpgCurrentChannelId)
                return True
        else:
            guifunc.listReset(listContainer)

        #Add items to list container
        guifunc.updateLabelText(self, 1, 'Zenders laden')
        guifunc.updateLabelText(self, 2, '[COLOR FF888888]Zenders worden geladen, nog even geduld...[/COLOR]')
        if lichanneltelevision.list_load_combined(listContainer, downloadRecordings=True) == False:
            guifunc.updateLabelText(self, 1, 'Niet beschikbaar')
            guifunc.updateLabelText(self, 2, '[COLOR FF888888]Zenders zijn niet beschikbaar.[/COLOR]')
            listContainer = self.getControl(1000)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectIndex(listContainer, 0)
            return False

        #Focus on the list container
        if listContainer.size() > 0:
            lifunc.focus_listcontainer_value(self, 1001, 0, True, 'ChannelId', var.EpgCurrentChannelId)
        else:
            #Set channel type string
            channelTypeString = 'zenders'
            if getset.setting_get('LoadChannelFavoritesOnly') == 'true':
                channelTypeString = 'favorieten zenders'

            #Update status label text
            listContainer = self.getControl(1000)
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.updateLabelText(self, 1, 'Geen zenders gevonden')
                guifunc.updateLabelText(self, 2, "[COLOR FF888888]Zender[/COLOR] " + var.SearchTermResult + " [COLOR FF888888]niet gevonden.[/COLOR]")
                guifunc.listSelectIndex(listContainer, 1)
            else:
                guifunc.updateLabelText(self, 1, 'Geen ' + channelTypeString)
                guifunc.updateLabelText(self, 2, "[COLOR FF888888]Geen beschikbare " + channelTypeString + ".[/COLOR]")
                guifunc.listSelectIndex(listContainer, 0)

            #Focus on navigation menu list
            guifunc.controlFocus(self, listContainer)

            #Reset the program list
            listContainer = self.getControl(1002)
            guifunc.listReset(listContainer)
            return False

        #Force manual epg update
        self.ChannelManualUpdate = True
        return True

    def load_programs(self, forceLoad=False, forceFocus=False):
        self.ProgramPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.load_programs_code(forceLoad, forceFocus)
        self.ProgramPauseUpdate = False

    def load_programs_code(self, forceLoad=False, forceFocus=False):
        #Set currently selected channel
        listContainer = self.getControl(1001)
        listItemSelected = listContainer.getSelectedItem()
        if listItemSelected == None:
            guifunc.updateLabelText(self, 1, 'Selecteer zender')
            guifunc.updateLabelText(self, 2, "[COLOR FF888888]Selecteer de gewenste televisie zender.[/COLOR]")
            return
        else:
            var.EpgCurrentChannelId = listItemSelected.getProperty('ChannelId')
            var.EpgCurrentChannelName = listItemSelected.getProperty('ChannelName')

        #Get and check the list container
        listContainer = self.getControl(1002)
        listItemCount = listContainer.size()

        #Check if channel has changed
        epgChannelChanged = var.EpgPreviousChannelId != var.EpgCurrentChannelId

        #Check epg day has changed
        epgDayTimeChanged = var.EpgPreviousLoadDateTime != var.EpgCurrentLoadDateTime

        #Check if update is needed
        if forceLoad or epgChannelChanged or epgDayTimeChanged or listItemCount == 0:
            #Clear current epg items
            guifunc.listReset(listContainer)
        else:
            #Keep current epg items
            return

        #Add items to list container
        guifunc.updateLabelText(self, 1, 'TV Gids laden')
        guifunc.updateLabelText(self, 2, '[COLOR FF888888]TV Gids wordt geladen, nog even geduld...[/COLOR]')
        if liepgload.list_load_combined(listContainer) == False:
            guifunc.updateLabelText(self, 1, 'Niet beschikbaar')
            guifunc.updateLabelText(self, 2, '[COLOR FF888888]TV Gids is niet beschikbaar.[/COLOR]')
            listContainer = self.getControl(1000)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectIndex(listContainer, 0)
            return

        #Select program index
        self.epg_selectindex_program(forceFocus)

        #Update the status
        self.count_epg()

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
        programSelectIndexSelect = 0

        #Check if program is airing or matches navigate index
        for itemNum in range(0, listItemCount):
            listItem = listContainer.getListItem(itemNum)

            #Check if program matches navigate id
            if var.EpgNavigateIdentifier == listItem.getProperty('ProgramId'):
                programSelectIndexNavigate = itemNum
                break

            #Check if program matches select id
            if var.EpgSelectIdentifier == listItem.getProperty('ProgramId'):
                programSelectIndexSelect = itemNum

            #Check if program is still to come
            if programSelectIndexUpcoming == 0 and listItem.getProperty('ProgramIsUpcoming') == 'true':
                programSelectIndexUpcoming = itemNum

            #Check if program is currently airing
            if listItem.getProperty('ProgramIsAiring') == 'true':
                programSelectIndexAiring = itemNum

        #Select program list item
        if programSelectIndexNavigate != 0:
            forceFocus = True
            guifunc.listSelectIndex(listContainer, programSelectIndexNavigate)
        elif programSelectIndexAiring != 0:
            guifunc.listSelectIndex(listContainer, programSelectIndexAiring)
        elif programSelectIndexUpcoming != 0:
            guifunc.listSelectIndex(listContainer, programSelectIndexUpcoming)
        elif programSelectIndexSelect != 0:
            guifunc.listSelectIndex(listContainer, programSelectIndexSelect)
        else:
            guifunc.listSelectIndex(listContainer, 0)

        #Focus on program list
        if forceFocus == True:
            guifunc.controlFocus(self, listContainer)

        #Reset navigate variable
        var.EpgNavigateIdentifier = ''

    #Update the status
    def count_epg(self):
        #Set loading day string
        loadDayString = func.day_string_from_datetime(var.EpgCurrentLoadDateTime)

        #Update the label texts
        listContainer = self.getControl(1002)
        if listContainer.size() == 0:
            if func.string_isnullorempty(var.SearchTermResult) == True:
                guifunc.updateLabelText(self, 1, "Geen programma's")
                guifunc.updateLabelText(self, 2, "[COLOR FF888888]Geen programma's beschikbaar voor[/COLOR] " + var.EpgCurrentChannelName + " [COLOR FF888888]op[/COLOR] " + loadDayString)
            else:
                guifunc.updateLabelText(self, 1, "Geen programma's gevonden")
                guifunc.updateLabelText(self, 2, "[COLOR FF888888]Programma[/COLOR] " + var.SearchTermResult + " [COLOR FF888888]niet gevonden op[/COLOR] " + loadDayString)
        else:
            if func.string_isnullorempty(var.SearchTermResult) == True:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " programma's")
                guifunc.updateLabelText(self, 2, "[COLOR FF888888]Alle programma's voor[/COLOR] " + var.EpgCurrentChannelName + " [COLOR FF888888]op[/COLOR] " + loadDayString)
            else:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " programma's gevonden")
                guifunc.updateLabelText(self, 2, "[COLOR FF888888]Programma's gevonden voor[/COLOR] " + var.SearchTermResult + " [COLOR FF888888]op[/COLOR] " + loadDayString)

    def thread_update_program_progress(self):
        threadLastTime = ''
        while var.thread_update_epg_program.Allowed(sleepDelayMs=1000):
            try:
                threadCurrentTime = datetime.now().strftime('%H:%M')
                if threadLastTime != threadCurrentTime or self.ProgramManualUpdate:
                    threadLastTime = threadCurrentTime
                    self.ProgramManualUpdate = False

                    #Update program status
                    self.update_program_status()
            except:
                pass

    def thread_update_channel_progress(self):
        threadLastTime = ''
        while var.thread_update_epg_channel.Allowed(sleepDelayMs=1000):
            try:
                threadCurrentTime = datetime.now().strftime('%H:%M')
                if threadLastTime != threadCurrentTime or self.ChannelManualUpdate:
                    threadLastTime = threadCurrentTime
                    self.ChannelManualUpdate = False

                    #Update channel status
                    self.update_channel_status()
            except:
                pass
