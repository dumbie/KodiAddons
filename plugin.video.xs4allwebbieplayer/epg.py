from datetime import datetime, timedelta
from threading import Thread
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
import stream
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
        #Stop the update progress thread
        var.thread_update_epg_progress = None

        #Close the shown window
        var.guiEpg.close()
        var.guiEpg = None

class Gui(xbmcgui.WindowXML):
    EpgManualUpdate = False

    def onInit(self):
        self.buttons_add_navigation()
        self.load_recording_event(False)
        self.load_recording_series(False)
        channelsLoaded = self.load_channels()
        if channelsLoaded == True:
            self.set_channel_epg_variables()
            self.load_programs()

            #Force manual epg update
            self.EpgManualUpdate = True

            #Start the epg update thread
            if var.thread_update_epg_progress == None:
                var.thread_update_epg_progress = Thread(target=self.thread_update_epg_progress)
                var.thread_update_epg_progress.start()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer == None:
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
                    listcontainer = self.getControl(1000)
                    self.setFocus(listcontainer)
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
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(listcontainer.getSelectedPosition() + 1)
            xbmc.sleep(100)
            self.set_channel_epg_variables()
            self.load_programs()
        elif actionId == var.ACTION_PREV_ITEM:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(listcontainer.getSelectedPosition() - 1)
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

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'),'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zoek naar zender')
        listitem.setProperty('Action', 'search_channel')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zoek programma')
        listitem.setProperty('Action', 'search_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Selecteer dag')
        listitem.setProperty('Action', 'set_load_day')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/calendar.png'),'icon': path.resources('resources/skins/default/media/common/calendar.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Alle of favorieten')
        listitem.setProperty('Action', 'switch_all_favorites')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/star.png'), 'icon': path.resources('resources/skins/default/media/common/star.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Vernieuwen')
        listitem.setProperty('Action', 'refresh_epg')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def focus_on_channel_list(self, forceFocus=False):
        if var.EpgCurrentChannelId == '':
            selectChannelId = var.addon.getSetting('CurrentChannelId')
        else:
            selectChannelId = var.EpgCurrentChannelId
        lifunc.focus_on_channelid_in_list(self, 1001, 0, forceFocus, selectChannelId)

    def focus_on_item_list(self):
        #Get and check channel list container
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            return

        #Get and check program list container
        listcontainer = self.getControl(1002)
        if listcontainer.size() > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            return

    def dialog_set_day(self):
        #Set dates to array
        dialogAnswers = []

        for x in range(var.VodDaysOffsetPast + var.EpgDaysOffsetFuture):
            dayString = func.day_string_from_day_offset(x - var.VodDaysOffsetPast)
            dialogAnswers.append(dayString)

        dialogHeader = 'Selecteer dag'
        dialogSummary = 'Selecteer de gewenste televisie gids dag.'
        dialogFooter = ''

        #Get day selection index
        selectIndex = var.VodDaysOffsetPast + -func.day_offset_from_datetime(var.EpgCurrentLoadDateTime)

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers, selectIndex)
        if dialogResult == 'DialogCancel':
            return

        #Calculate selected day offset
        selectedIndex = (dialogAnswers.index(dialogResult) - var.VodDaysOffsetPast)

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

        #Check if the current program is airing
        dateTimeNow = datetime.now()
        if var.RecordingAccess == True:
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
            stream.switch_channel_tv_listitem(listItemSelected, False, False)
        elif dialogResult == 'Programma terug kijken':
            stream.play_stream_program(listItemSelected, False)
        elif dialogResult == 'Toon alle zenders' or dialogResult == 'Toon favorieten zenders':
            self.switch_all_favorites()

    def switch_all_favorites(self):
        try:
            #Switch favorites mode on or off
            if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
                var.addon.setSetting('LoadChannelFavoritesOnly', 'false')
            else:
                #Check if there are favorites set
                if var.FavoriteTelevisionDataJson == []:
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
        listcontainer = self.getControl(1001)
        listitemcount = listcontainer.size()

        #Update all channel status icons
        for itemNum in range(0, listitemcount):
            try:
                updateItem = listcontainer.getListItem(itemNum)
                liepgupdate.list_update_channel(updateItem)
            except:
                pass

    def update_program_status(self):
        #Get and check the list container
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Update all program progress and status
        for itemNum in range(0, listitemcount):
            try:
                updateItem = listcontainer.getListItem(itemNum)
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
            self.EpgManualUpdate = True
        elif alarmAdded == 'Remove':
            #Force manual epg update
            self.EpgManualUpdate = True

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
        listcontainer = self.getControl(1001)
        listItemSelected = listcontainer.getSelectedItem()
        if listItemSelected == None:
            func.updateLabelText(self, 1, 'Selecteer zender')
            func.updateLabelText(self, 2, "[COLOR gray]Selecteer de gewenste televisie zender.[/COLOR]")
            return

        var.EpgCurrentChannelId = listItemSelected.getProperty('ChannelId')
        var.EpgCurrentExternalId = listItemSelected.getProperty('ExternalId')
        var.EpgCurrentChannelName = listItemSelected.getProperty('ChannelName')

    def load_channels(self, forceLoad=False):
        #Get and check the list container
        listcontainer = self.getControl(1001)
        if forceLoad == False:
            if listcontainer.size() > 0:
                self.focus_on_channel_list(False)
                return True
        else:
            listcontainer.reset()

        #Download the channels
        func.updateLabelText(self, 1, 'Zenders downloaden')
        func.updateLabelText(self, 2, '[COLOR gray]Zenders worden gedownload, nog even geduld...[/COLOR]')
        downloadResult = download.download_channels_tv(False)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            func.updateLabelText(self, 2, '[COLOR gray]TV Gids is niet beschikbaar.[/COLOR]')
            listcontainer = self.getControl(1000)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, 'Zenders laden')
        func.updateLabelText(self, 2, '[COLOR gray]Zenders worden geladen, nog even geduld...[/COLOR]')

        #Add items to sort list
        listcontainersort = []
        lichanneltelevision.list_load(listcontainersort)

        #Sort and add items to container
        listcontainer.addItems(listcontainersort)

        #Focus on the list container
        if listcontainer.size() > 0:
            self.focus_on_channel_list(True)
        else:
            #Set channel type string
            channelTypeString = 'zenders'
            if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
                channelTypeString = 'favorieten zenders'

            #Update status label text
            listcontainer = self.getControl(1000)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                func.updateLabelText(self, 2, "[COLOR gray]Zender[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]niet gevonden.[/COLOR]")
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen ' + channelTypeString)
                func.updateLabelText(self, 2, "[COLOR gray]Geen beschikbare " + channelTypeString + ".[/COLOR]")
                listcontainer.selectItem(0)
            xbmc.sleep(100)

            #Focus on channel list
            self.setFocus(listcontainer)
            xbmc.sleep(100)

            #Reset the program list
            listcontainer = self.getControl(1002)
            listcontainer.reset()
            return False

        #Force manual epg update
        self.EpgManualUpdate = True

        return True

    def load_recording_event(self, forceUpdate=False):
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False: return False

    def load_recording_series(self, forceUpdate=False):
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False: return False

    def load_programs(self, forceUpdate=False, forceLoad=False, forceFocus=False):
        #Get and check the list container
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Check if channel has changed
        epgChannelChanged = var.EpgPreviousChannelId != var.EpgCurrentChannelId

        #Check epg day has changed
        epgDayTimeChanged = var.EpgPreviousLoadDateTime != var.EpgCurrentLoadDateTime

        #Check if update is needed
        if forceLoad or forceUpdate or epgChannelChanged or epgDayTimeChanged or listitemcount == 0:
            #Clear the current epg items
            listcontainer.reset()

            #Download the epg day information
            func.updateLabelText(self, 1, 'Gids download')
            func.updateLabelText(self, 2, '[COLOR gray]TV Gids wordt gedownload, nog even geduld...[/COLOR]')
            var.EpgCurrentDayJson = download.download_epg_day(var.EpgCurrentLoadDateTime, forceUpdate)
            if var.EpgCurrentDayJson == None:
                func.updateLabelText(self, 1, 'Niet beschikbaar')
                func.updateLabelText(self, 2, '[COLOR gray]TV Gids is niet beschikbaar.[/COLOR]')
                listcontainer = self.getControl(1000)
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
                return
        else:
            return

        #Update epg status
        func.updateLabelText(self, 1, 'Gids laden')
        func.updateLabelText(self, 2, '[COLOR gray]TV Gids wordt geladen, nog even geduld...[/COLOR]')

        listcontainersort = []
        if func.string_isnullorempty(var.SearchChannelTerm):
            #Load programs for set day and channel
            channelEpgJson = metadatafunc.search_channelid_jsonepg(var.EpgCurrentDayJson, var.EpgCurrentChannelId)
            if channelEpgJson == None:
                func.updateLabelText(self, 1, 'Zender gids mist')
                func.updateLabelText(self, 2, '[COLOR gray]TV Gids is niet beschikbaar voor[/COLOR] ' + var.EpgCurrentChannelName)
                return

            #Add items to sort list
            liepgload.list_load(listcontainersort, channelEpgJson)
        else:
            #Load programs for search term from all channels
            for channelEpgJson in var.EpgCurrentDayJson["resultObj"]["containers"]:
                #Add items to sort list
                liepgload.list_load(listcontainersort, channelEpgJson)

        #Sort and add items to container
        listcontainersort.sort(key=lambda x: x.getProperty('ProgramTimeStart'))
        listcontainer.addItems(listcontainersort)

        #Select program index
        self.epg_selectindex_program(forceFocus)

        #Update the status
        self.count_epg(var.EpgCurrentChannelName)

        #Force manual epg update
        self.EpgManualUpdate = True

        #Update epg variables
        var.EpgPreviousChannelId = var.EpgCurrentChannelId
        var.EpgPreviousLoadDateTime = var.EpgCurrentLoadDateTime

    #Epg program select index
    def epg_selectindex_program(self, forceFocus=False):
        #Get and check the list container
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Check program list item count
        if listitemcount == 0: return

        programSelectIndexAiring = 0
        programSelectIndexUpcoming = 0
        programSelectIndexNavigate = 0

        #Check if program is airing or matches navigate index
        for itemNum in range(0, listitemcount):
            listitem = listcontainer.getListItem(itemNum)

            #Check if program matches navigate id
            if var.EpgNavigateProgramId == listitem.getProperty('ProgramId'):
                programSelectIndexNavigate = itemNum
                break

            #Check if program is still to come
            if programSelectIndexUpcoming == 0 and listitem.getProperty('ProgramIsUpcoming') == 'true':
                programSelectIndexUpcoming = itemNum

            #Check if program is currently airing
            if listitem.getProperty('ProgramIsAiring') == 'true':
                programSelectIndexAiring = itemNum

        #Select program list item
        if programSelectIndexNavigate != 0:
            forceFocus = True
            listcontainer.selectItem(programSelectIndexNavigate)
        elif programSelectIndexAiring != 0:
            listcontainer.selectItem(programSelectIndexAiring)
        elif programSelectIndexUpcoming != 0:
            listcontainer.selectItem(programSelectIndexUpcoming)
        else:
            listcontainer.selectItem(0)
        xbmc.sleep(100)

        #Focus on program list
        if forceFocus:
            self.setFocus(listcontainer)
            xbmc.sleep(100)

        #Reset navigate variable
        var.EpgNavigateProgramId = ''

    #Update the status
    def count_epg(self, ChannelName):
        #Set loading day string
        loadDayString = func.day_string_from_datetime(var.EpgCurrentLoadDateTime)

        #Update the label texts
        listcontainer = self.getControl(1002)
        if listcontainer.size() == 0:
            if var.SearchChannelTerm == '':
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 2, "[COLOR gray]Geen programma's beschikbaar voor[/COLOR] " + ChannelName + " [COLOR gray]op[/COLOR] " + loadDayString)
            else:
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 2, "[COLOR gray]Programma[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]niet gevonden op[/COLOR] " + loadDayString)
        else:
            if var.SearchChannelTerm == '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's")
                func.updateLabelText(self, 2, "[COLOR gray]Alle programma's voor[/COLOR] " + ChannelName + " [COLOR gray]op[/COLOR] " + loadDayString)
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 2, "[COLOR gray]Programma's gevonden voor[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]op[/COLOR] " + loadDayString)

    def thread_update_epg_progress(self):
        threadLastTime = (datetime.now() - timedelta(minutes=1)).strftime('%H:%M')
        while var.thread_update_epg_progress != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime or self.EpgManualUpdate:
                threadLastTime = threadCurrentTime
                self.EpgManualUpdate = False

                #Update channel status
                self.update_channel_status()

                #Update program status
                self.update_program_status()
            else:
                xbmc.sleep(1000)
