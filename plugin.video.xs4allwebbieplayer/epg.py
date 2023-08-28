from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import alarm
import lichanneltelevision
import dialog
import download
import favorite
import func
import metadatainfo
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
    def onInit(self):
        self.buttons_add_navigation()
        self.load_recording_event(False)
        self.load_recording_series(False)
        favorite.favorite_json_load()
        channelsLoaded = self.load_channels()
        if channelsLoaded == True:
            self.set_channel_epg_variables()
            self.load_epg()

            #Start the update progress thread
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
                elif listItemAction == "refresh_epg":
                    self.load_epg(True)
            elif clickId == 1001:
                self.set_channel_epg_variables()
                self.load_epg()
            elif clickId == 1002:
                self.dialog_alarm_record(clickedControl)
            elif clickId == 9000:
                if xbmc.Player().isPlayingVideo():
                    var.PlayerCustom.Fullscreen(True)
                else:
                    listcontainer = self.getControl(1000)
                    self.setFocus(listcontainer)
                    xbmc.sleep(100)
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
            self.load_epg()
        elif actionId == var.ACTION_PREV_ITEM:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(listcontainer.getSelectedPosition() - 1)
            xbmc.sleep(100)
            self.set_channel_epg_variables()
            self.load_epg()
        elif actionId == var.ACTION_PLAYER_PLAY:
            self.dialog_set_day()
        elif actionId == var.ACTION_PLAYER_FORWARD:
            self.dialog_set_day()
        elif actionId == var.ACTION_PLAYER_REWIND:
            self.dialog_set_day()
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_program()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM):
            clickedControl = self.getControl(1002)
            self.dialog_alarm_record(clickedControl)
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

        listitem = xbmcgui.ListItem('Vernieuwen')
        listitem.setProperty('Action', 'refresh_epg')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

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
        self.load_epg()

    def dialog_alarm_record(self, clickedControl):
        listItemSelected = clickedControl.getSelectedItem()
        ProgramTimeStartString = listItemSelected.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartString, '%Y-%m-%d %H:%M:%S')
        ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
        ProgramTimeEndString = listItemSelected.getProperty('ProgramTimeEnd')
        ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndString, '%Y-%m-%d %H:%M:%S')
        ProgramName = listItemSelected.getProperty('ProgramName')

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
                dialogSummary = ProgramName + ' kijken?'
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
        if var.LoadChannelFavoritesOnly == True:
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
            self.switch_allfavorites()

    def switch_allfavorites(self):
        try:
            #Switch favorites mode on or off
            if var.LoadChannelFavoritesOnly == True:
                var.LoadChannelFavoritesOnly = False
            else:
                #Check if there are favorites set
                if var.FavoriteTelevisionDataJson == []:
                    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
                    xbmcgui.Dialog().notification(var.addonname, 'Geen favorieten zenders.', notificationIcon, 2500, False)
                    return
                var.LoadChannelFavoritesOnly = True

            channelsLoaded = self.load_channels(True)
            if channelsLoaded == True:
                self.set_channel_epg_variables()
                self.load_epg(False, True)
        except:
            pass

    def update_program_record_event(self):
        #Get the epg list control
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Check if program has active recording
        for itemNum in range(0, listitemcount):
            updateItem = listcontainer.getListItem(itemNum)
            ProgramId = updateItem.getProperty('ProgramId')
            ProgramTimeEndString = updateItem.getProperty('ProgramTimeEnd')
            ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndString, '%Y-%m-%d %H:%M:%S')

            #Check if program is recording event and if the recording is planned or done
            recordProgramEvent = func.search_programid_jsonrecording_event(ProgramId)
            if recordProgramEvent:
                if datetime.now() > ProgramTimeEndDateTime:
                    updateItem.setProperty('ProgramRecordEventPlanned', 'false')
                    updateItem.setProperty('ProgramRecordEventDone', 'true')
                else:
                    updateItem.setProperty('ProgramRecordEventPlanned', 'true')
                    updateItem.setProperty('ProgramRecordEventDone', 'false')
                updateItem.setProperty('ProgramRecordEventId', metadatainfo.contentId_from_json_metadata(recordProgramEvent))
                updateItem.setProperty('ProgramStartDeltaTime', str(metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent)))
            else:
                updateItem.setProperty('ProgramRecordEventPlanned', 'false')
                updateItem.setProperty('ProgramRecordEventDone', 'false')
                updateItem.setProperty('ProgramRecordEventId', '')
                updateItem.setProperty('ProgramStartDeltaTime', '0')

    def update_program_record_series(self):
        #Get the epg list control
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Check if program has active recording
        for itemNum in range(0, listitemcount):
            updateItem = listcontainer.getListItem(itemNum)
            ProgramRecordSeriesId = updateItem.getProperty('ProgramRecordSeriesId')

            #Check if program is recording series
            recordProgramSeries = func.search_seriesid_jsonrecording_series(ProgramRecordSeriesId)
            if recordProgramSeries:
                updateItem.setProperty('ProgramRecordSeries', 'true')
            else:
                updateItem.setProperty('ProgramRecordSeries', 'false')

    def update_channel_record_event_icon(self, ChannelId):
        #Get the channel list control
        listcontainer = self.getControl(1001)
        listItemSelected = listcontainer.getSelectedItem()

        #Check if channel has active recording
        if func.search_channelid_jsonrecording_event(ChannelId, True):
            listItemSelected.setProperty('ChannelRecordEvent', 'true')
        else:
            listItemSelected.setProperty('ChannelRecordEvent', 'false')

    def update_channel_record_series_icon(self, ChannelId):
        #Get the channel list control
        listcontainer = self.getControl(1001)
        listItemSelected = listcontainer.getSelectedItem()

        #Check if channel has active recording series
        if func.search_channelid_jsonrecording_series(ChannelId):
            listItemSelected.setProperty('ChannelRecordSeries', 'true')
        else:
            listItemSelected.setProperty('ChannelRecordSeries', 'false')

    def update_channel_alarm_icon(self, ChannelId):
        #Get the channel list control
        listcontainer = self.getControl(1001)
        listItemSelected = listcontainer.getSelectedItem()

        #Check if channel has active alarm
        if alarm.alarm_duplicate_channel_check(ChannelId) == True:
            listItemSelected.setProperty('ChannelAlarm', 'true')
        else:
            listItemSelected.setProperty('ChannelAlarm', 'false')

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
            listItemSelected.setProperty('ProgramAlarm', 'true')
            self.update_channel_alarm_icon(ChannelId)
        elif alarmAdded == 'Remove':
            listItemSelected.setProperty('ProgramAlarm', 'false')
            self.update_channel_alarm_icon(ChannelId)

    def search_channel(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek naar zender', True)

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        channelsLoaded = self.load_channels(True)
        var.SearchFilterTerm = ''
        if channelsLoaded == True:
            self.set_channel_epg_variables()
            self.load_epg(False, True)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek programma')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_epg(False, True)
        var.SearchFilterTerm = ''

    def set_channel_epg_variables(self):
        #Set the currently selected channel
        listcontainer = self.getControl(1001)
        listItemSelected = listcontainer.getSelectedItem()
        if listItemSelected == None:
            func.updateLabelText(self, 1, 'Selecteer zender')
            func.updateLabelText(self, 2, "Selecteer een zender om de programma's voor weer te geven.")
            return

        var.EpgCurrentAssetId = listItemSelected.getProperty('AssetId')
        var.EpgCurrentChannelId = listItemSelected.getProperty('ChannelId')
        var.EpgCurrentExternalId = listItemSelected.getProperty('ExternalId')
        var.EpgCurrentChannelName = listItemSelected.getProperty('ChannelName')

    def select_channel_epg(self, forceFocus=False):
        if var.EpgCurrentChannelId == '':
            selectChannelId = var.addon.getSetting('CurrentChannelId')
        else:
            selectChannelId = var.EpgCurrentChannelId
        func.focus_on_channel_list(self, 1001, 0, forceFocus, selectChannelId)

    def load_channels(self, forceLoad=False):
        #Get and check the list container
        listcontainer = self.getControl(1001)
        if forceLoad == False:
            if listcontainer.size() > 0:
                self.select_channel_epg(False)
                return True
        else:
            listcontainer.reset()

        #Download the channels
        func.updateLabelText(self, 1, 'Zenders downloaden')
        func.updateLabelText(self, 2, 'Zenders worden gedownload, nog even geduld...')
        downloadResult = download.download_channels_tv(False)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            func.updateLabelText(self, 2, 'TV Gids is niet beschikbaar.')
            listcontainer = self.getControl(1000)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Add channels to list
        func.updateLabelText(self, 1, 'Zenders laden')
        func.updateLabelText(self, 2, 'Zenders worden geladen, nog even geduld...')
        lichanneltelevision.list_load(listcontainer, True)

        #Focus on the list container
        if listcontainer.size() > 0:
            self.select_channel_epg(True)
            return True
        else:
            listcontainer = self.getControl(1000)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                func.updateLabelText(self, 2, "[COLOR gray]Zender[/COLOR] " + var.SearchFilterTerm + " [COLOR gray]niet gevonden om de programma's voor weer te geven.[/COLOR]")
                listcontainer.selectItem(1)
            elif var.LoadChannelFavoritesOnly == True:
                func.updateLabelText(self, 1, 'Geen favorieten zenders')
                func.updateLabelText(self, 2, "Geen favorieten zenders om de programma's voor weer te geven.")
                listcontainer.selectItem(0)
            else:
                func.updateLabelText(self, 1, 'Geen zenders')
                func.updateLabelText(self, 2, "Geen zenders om de programma's voor weer te geven.")
                listcontainer.selectItem(0)
            xbmc.sleep(100)

            #Reset the program list
            listcontainer = self.getControl(1002)
            listcontainer.reset()
            return False

    def load_recording_event(self, forceUpdate=False):
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False: return False

    def load_recording_series(self, forceUpdate=False):
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False: return False

    def load_progress(self):
        #Get and check the list container
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Clear expired alarms from Json
        alarm.alarm_clean_expired()

        #Update the selected channel alarm icon
        self.update_channel_alarm_icon(var.EpgCurrentChannelId)

        #Update the selected channel recording event icon
        self.update_channel_record_event_icon(var.EpgCurrentChannelId)

        #Update the selected channel recording series icon
        self.update_channel_record_series_icon(var.EpgCurrentChannelId)

        #Generate program progress for programs
        for itemNum in range(0, listitemcount):
            try:
                updateItem = listcontainer.getListItem(itemNum)
                liepgupdate.list_update(updateItem)
            except:
                pass

    def load_epg(self, forceUpdate=False, forceLoad=False):
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

            #Set the day string
            loadDayString = func.day_string_from_datetime(var.EpgCurrentLoadDateTime, False)

            #Download the epg day information
            func.updateLabelText(self, 1, 'Gids download')
            func.updateLabelText(self, 2, '[COLOR gray]TV Gids voor[/COLOR] ' + loadDayString + ' [COLOR gray]wordt gedownload, nog even geduld...[/COLOR]')
            var.EpgCurrentDayJson = download.download_epg_day(var.EpgCurrentLoadDateTime, forceUpdate)
            if var.EpgCurrentDayJson == None:
                func.updateLabelText(self, 1, 'Niet beschikbaar')
                func.updateLabelText(self, 2, 'TV Gids is niet beschikbaar.')
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
        func.updateLabelText(self, 2, 'TV Gids wordt geladen, nog even geduld...')

        #Get epg json for set day and channel
        channelEpgJson = func.search_channelid_jsonepg(var.EpgCurrentDayJson, var.EpgCurrentChannelId)
        if channelEpgJson == None:
            func.updateLabelText(self, 1, 'Zender gids mist')
            func.updateLabelText(self, 2, '[COLOR gray]TV Gids is niet beschikbaar voor[/COLOR] ' + var.EpgCurrentChannelName)
            return

        #Add programs to list
        liepgload.list_load(listcontainer, channelEpgJson)

        #Select program index
        self.epg_selectindex_program()

        #Load program progress
        self.load_progress()

        #Update the status
        self.count_epg(var.EpgCurrentChannelName)

        #Update epg variables
        var.EpgPreviousChannelId = var.EpgCurrentChannelId
        var.EpgPreviousLoadDateTime = var.EpgCurrentLoadDateTime

    #Epg program select index
    def epg_selectindex_program(self):
        #Get and check the list container
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        programSelectIndexAiring = 0
        programSelectIndexNavigate = 0

        #Check if program is airing or matches navigate index
        for itemNum in range(0, listitemcount):
            listitem = listcontainer.getListItem(itemNum)

            #Check if program is currently airing
            if listitem.getProperty('ProgramIsAiring') == 'true':
                programSelectIndexAiring = itemNum

            #Check if program matches navigate id
            if var.EpgNavigateProgramId == listitem.getProperty('ProgramId'):
                programSelectIndexNavigate = itemNum
                break

        #Focus and select program list item
        if programSelectIndexNavigate != 0:
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(programSelectIndexNavigate)
        else:
            listcontainer.selectItem(programSelectIndexAiring)
        var.EpgNavigateProgramId = ''
        xbmc.sleep(100)

    #Update the status
    def count_epg(self, ChannelName):
        #Set the day string
        loadDayString = func.day_string_from_datetime(var.EpgCurrentLoadDateTime)

        #Update the label texts
        listcontainer = self.getControl(1002)
        if listcontainer.size() == 0:
            if var.SearchFilterTerm == '':
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 2, "[COLOR gray]Geen programma's beschikbaar voor[/COLOR] " + loadDayString + " [COLOR gray]op[/COLOR] " + ChannelName)
            else:
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 2, "[COLOR gray]Programma[/COLOR] " + var.SearchFilterTerm + " [COLOR gray]niet gevonden voor[/COLOR] " + loadDayString + " [COLOR gray]op[/COLOR] " + ChannelName)
        else:
            if var.SearchFilterTerm == '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's")
                func.updateLabelText(self, 2, "[COLOR gray]Alle programma's voor[/COLOR] " + loadDayString + " [COLOR gray]op[/COLOR] " + ChannelName)
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 2, var.SearchFilterTerm + " [COLOR gray]gevonden voor[/COLOR] " + loadDayString + " [COLOR gray]op[/COLOR] " + ChannelName)

    def thread_update_epg_progress(self):
        threadLastTime = (datetime.now() - timedelta(minutes=1)).strftime('%H:%M')
        while var.thread_update_epg_progress != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime:
                threadLastTime = threadCurrentTime
                #Load program progress
                self.load_progress()
            else:
                xbmc.sleep(2000)
