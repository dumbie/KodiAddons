from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import alarm
import channellist
import dialog
import download
import favorite
import func
import hybrid
import metadatainfo
import path
import stream
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
    EpgCurrentLoadDayInt = 0
    EpgPreviousLoadDayInt = 9999
    EpgPreviousLoadDateTime = '1970-01-01'
    EpgCurrentDayJson = []
    EpgCurrentAssetId = ''
    EpgCurrentChannelId = ''
    EpgCurrentExternalId = ''
    EpgCurrentChannelName = ''
    EpgPreviousChannelId = ''

    def onInit(self):
        self.buttons_add_navigation()
        self.load_recording_event(False)
        self.load_recording_series(False)
        favorite.favorite_json_load()
        channelsLoaded = self.load_channels()
        if channelsLoaded:
            self.set_channel_epg()
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
                elif listItemAction == "search_channelprogram":
                    self.search_channelprogram()
                elif listItemAction == "refresh_epg":
                    self.load_epg(True)
            elif clickId == 1001:
                self.set_channel_epg()
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
            self.set_channel_epg()
            self.load_epg()
        elif actionId == var.ACTION_PREV_ITEM:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(listcontainer.getSelectedPosition() - 1)
            xbmc.sleep(100)
            self.set_channel_epg()
            self.load_epg()
        elif actionId == var.ACTION_PLAYER_PLAY:
            self.dialog_set_day()
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_channelprogram()
        elif actionId == var.ACTION_PLAYER_FORWARD:
            self.switch_epg_day(True)
        elif actionId == var.ACTION_PLAYER_REWIND:
            self.switch_epg_day(False)
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
        listitem.setProperty('Action', 'search_channelprogram')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Selecteer gids dag')
        listitem.setProperty('Action', 'set_load_day')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/calendar.png'),'icon': path.resources('resources/skins/default/media/common/calendar.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Vernieuwen')
        listitem.setProperty('Action', 'refresh_epg')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def string_day_number(self, numberDay):
        todayDateTime = datetime.today().date()
        dayDateTime = todayDateTime + timedelta(days=numberDay)
        dayString = dayDateTime.strftime('%a, %d %B %Y')

        if dayDateTime == todayDateTime + timedelta(days=2):
            dayString += ' (Overmorgen)'
        elif dayDateTime == todayDateTime + timedelta(days=1):
            dayString += ' (Morgen)'
        elif dayDateTime == todayDateTime:
            dayString += ' (Vandaag)'
        elif dayDateTime == todayDateTime + timedelta(days=-1):
            dayString += ' (Gisteren)'
        elif dayDateTime == todayDateTime + timedelta(days=-2):
            dayString += ' (Eergister)'

        return dayString

    def dialog_set_day(self):
        #Set dates to array
        dialogAnswers = []

        for x in range(var.EpgDaysOffsetPast + var.EpgDaysOffsetFuture):
            dayString = self.string_day_number(x - var.EpgDaysOffsetPast)
            dialogAnswers.append(dayString)

        dialogHeader = 'Televisie gids dag'
        dialogSummary = 'Selecteer de gewenste televisie gids dag.'
        dialogFooter = ''

        selectIndex = self.EpgCurrentLoadDayInt + var.EpgDaysOffsetPast
        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers, selectIndex)
        if dialogResult == 'DialogCancel':
            return

        #Calculate epg day offset
        self.EpgCurrentLoadDayInt = (dialogAnswers.index(dialogResult) - var.EpgDaysOffsetPast)

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

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Alarm zetten of annuleren':
            self.set_program_alarm(listItemSelected)
        elif dialogResult == 'Programma opnemen of annuleren':
            self.set_program_record(listItemSelected)
        elif dialogResult == 'Live programma kijken':
            stream.switch_channel_tv_listitem(listItemSelected, False, False)
        elif dialogResult == 'Programma terug kijken':
            stream.play_stream_program(listItemSelected, False)
        elif dialogResult == 'Serie seizoen opnemen of annuleren':
            self.set_series_record(listItemSelected, False)

    def update_program_record_event(self):
        #Get the epg list control
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Check if program has active recording
        for channelNum in range(0, listitemcount):
            updateItem = listcontainer.getListItem(channelNum)
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
        for channelNum in range(0, listitemcount):
            updateItem = listcontainer.getListItem(channelNum)
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

    def set_series_record(self, listItemSelected, forceRecord=False):
        ChannelId = listItemSelected.getProperty('ChannelId')
        ProgramRecordSeries = listItemSelected.getProperty('ProgramRecordSeries')
        ProgramRecordSeriesId = listItemSelected.getProperty('ProgramRecordSeriesId')

        if ProgramRecordSeriesId == '':
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen kan niet worden opgenomen.', notificationIcon, 2500, False)
            return

        if ProgramRecordSeries == 'false' or forceRecord == True:
            seriesAdd = download.record_series_add(ChannelId, ProgramRecordSeriesId)
            if seriesAdd == True:
                self.update_channel_record_event_icon(ChannelId)
                self.update_program_record_event()
                self.update_channel_record_series_icon(ChannelId)
                self.update_program_record_series()
        else:
            #Get the removal series id
            recordProgramSeries = func.search_seriesid_jsonrecording_series(ProgramRecordSeriesId)
            if recordProgramSeries:
                ProgramRecordSeriesIdLive = metadatainfo.seriesId_from_json_metadata(recordProgramSeries)
            else:
                notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
                xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt.', notificationIcon, 2500, False)
                return

            #Ask user to remove recordings
            dialogAnswers = ['Opnames verwijderen', 'Opnames houden']
            dialogHeader = 'Serie opnames verwijderen'
            dialogSummary = 'Wilt u ook alle opnames van deze serie seizoen verwijderen?'
            dialogFooter = ''
            dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
            if dialogResult == 'Opnames verwijderen':
                KeepRecording = False
            elif dialogResult == 'Opnames houden': 
                KeepRecording = True
            else:
                return

            #Remove record series
            seriesRemove = download.record_series_remove(ProgramRecordSeriesIdLive, KeepRecording)
            if seriesRemove == True:
                self.update_channel_record_event_icon(ChannelId)
                self.update_program_record_event()
                self.update_channel_record_series_icon(ChannelId)
                self.update_program_record_series()

    def set_program_record(self, listItemSelected, forceRecord=False):
        ChannelId = listItemSelected.getProperty('ChannelId')
        ProgramId = listItemSelected.getProperty('ProgramId')
        ProgramRecordEventId = listItemSelected.getProperty('ProgramRecordEventId')
        ProgramStartDeltaTime = listItemSelected.getProperty('ProgramStartDeltaTime')

        #Check if recording is already set
        if ProgramRecordEventId == '' or forceRecord == True:
            recordAdd = download.record_program_add(ProgramId)
            if recordAdd != '':
                self.update_channel_record_event_icon(ChannelId)
                self.update_program_record_event()
                self.update_channel_record_series_icon(ChannelId)
                self.update_program_record_series()
        else:
            recordRemove = download.record_program_remove(ProgramRecordEventId, ProgramStartDeltaTime)
            if recordRemove == True:
                self.update_channel_record_event_icon(ChannelId)
                self.update_program_record_event()
                self.update_channel_record_series_icon(ChannelId)
                self.update_program_record_series()

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

    def switch_epg_day(self, dayForward):
        if dayForward:
            if self.EpgCurrentLoadDayInt < (var.EpgDaysOffsetFuture - 1):
                self.EpgCurrentLoadDayInt = self.EpgCurrentLoadDayInt + 1
                self.load_epg()
        else:
            if self.EpgCurrentLoadDayInt > (var.EpgDaysOffsetPast * -1):
                self.EpgCurrentLoadDayInt = self.EpgCurrentLoadDayInt - 1
                self.load_epg()

    def search_channelprogram(self):
        try:
            keyboard = xbmc.Keyboard('default', 'heading')
            keyboard.setHeading('Zoek naar zender')
            keyboard.setDefault('')
            keyboard.setHiddenInput(False)
            keyboard.doModal()
            if keyboard.isConfirmed() == True:
                var.SearchFilterTerm = func.search_filter_string(keyboard.getText())
                channelsLoaded = self.load_channels(True)
                if channelsLoaded == True:
                    self.set_channel_epg()
                    self.load_epg()
        except:
            pass
        var.SearchFilterTerm = ''

    def set_channel_epg(self):
        #Set the currently selected channel
        listcontainer = self.getControl(1001)
        listItemSelected = listcontainer.getSelectedItem()
        if listItemSelected == None:
            func.updateLabelText(self, 1, 'Selecteer zender')
            func.updateLabelText(self, 2, "Selecteer een zender om de programma's voor weer te geven.")
            return

        self.EpgCurrentAssetId = listItemSelected.getProperty('AssetId')
        self.EpgCurrentChannelId = listItemSelected.getProperty('ChannelId')
        self.EpgCurrentExternalId = listItemSelected.getProperty('ExternalId')
        self.EpgCurrentChannelName = listItemSelected.getProperty('ChannelName')

    def select_channel_live(self):
        #Select current live channel
        if var.PlayerOverlay == True:
            currentChannelId = var.addon.getSetting('CurrentChannelId')
            func.focus_on_channel_list(self, 1001, 0, False, currentChannelId)

    def load_channels(self, forceLoad=False):
        #Get and check the list container
        listcontainer = self.getControl(1001)
        if forceLoad == False:
            if listcontainer.size() > 0:
                self.select_channel_live()
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
        channellist.channel_list_load(listcontainer, True)

        #Focus on the list container
        if listcontainer.size() > 0:
            currentChannelId = var.addon.getSetting('CurrentChannelId')
            func.focus_on_channel_list(self, 1001, 0, True, currentChannelId)
            return True
        else:
            listcontainer = self.getControl(1000)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                func.updateLabelText(self, 2, "Geen zender om de programma's voor weer te geven gevonden.")
                listcontainer.selectItem(1)
            elif var.LoadChannelFavoritesOnly == True:
                func.updateLabelText(self, 1, 'Geen favorieten zenders')
                func.updateLabelText(self, 2, "Geen zender om de programma's voor weer te geven gevonden.")
                listcontainer.selectItem(0)
            else:
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                func.updateLabelText(self, 2, "Geen zender om de programma's voor weer te geven gevonden.")
                listcontainer.selectItem(0)
            xbmc.sleep(100)

            #Reset the program list
            listcontainer = self.getControl(1002)
            listcontainer.reset()
            return False

    def load_recording_event(self, forceUpdate=False, silentUpdate=False):
        if silentUpdate == False:
            func.updateLabelText(self, 1, 'Opnames downloaden')
            func.updateLabelText(self, 2, 'Opnames worden gedownload, nog even geduld...')

        #Download the recording programs
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False: return False

    def load_recording_series(self, forceUpdate=False, silentUpdate=False):
        if silentUpdate == False:
            func.updateLabelText(self, 1, 'Series downloaden')
            func.updateLabelText(self, 2, 'Series worden gedownload, nog even geduld...')

        #Download the recording programs
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False: return False

    def load_progress(self):
        #Get and check the list container
        listcontainer = self.getControl(1002)
        listitemcount = listcontainer.size()

        #Clear expired alarms from Json
        alarm.alarm_clean_expired()

        #Generate program progress for programs
        dateTimeNow = datetime.now()
        for programNum in range(0, listitemcount):
            try:
                #Get program information list item
                updateItem = listcontainer.getListItem(programNum)
                ChannelId = updateItem.getProperty('ChannelId')
                ProgramId = updateItem.getProperty('ProgramId')
                ProgramName = updateItem.getProperty('ProgramName')
                ProgramDescriptionRaw = updateItem.getProperty('ProgramDescriptionRaw')
                ProgramDetailsProp = updateItem.getProperty('ProgramDetails')
                ProgramRecordSeriesId = updateItem.getProperty('ProgramRecordSeriesId')
                ProgramTimeStartProp = updateItem.getProperty('ProgramTimeStart')
                ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartProp, '%Y-%m-%d %H:%M:%S')
                ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
                ProgramTimeEndProp = updateItem.getProperty('ProgramTimeEnd')
                ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndProp, '%Y-%m-%d %H:%M:%S')
                ProgramTimeEndString = ProgramTimeEndDateTime.strftime('%H:%M')
                ProgramTimeLeftMinutes = int((ProgramTimeEndDateTime - dateTimeNow).total_seconds() / 60)
                ProgramTimeLeftString = str(ProgramTimeLeftMinutes)
                ProgramDurationString = updateItem.getProperty('ProgramDuration')

                #Update program progress
                ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))

                #Set program duration text
                if ProgramDurationString == '0':
                    ProgramTimingEpgList = ' onbekend programmaduur'
                    ProgramTimingDescription = ' onbekend programmaduur'
                if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
                    if ProgramTimeLeftString == '0':
                        ProgramTimingEpgList = ' is bijna afgelopen, duurde ' + ProgramDurationString + ' minuten'
                        ProgramTimingDescription = ' is bijna afgelopen, duurde ' + ProgramDurationString + ' minuten, begon om ' + ProgramTimeStartString
                    else:
                        ProgramTimingEpgList = ' duurt nog ' + ProgramTimeLeftString + ' van de ' + ProgramDurationString + ' minuten'
                        ProgramTimingDescription = ' duurt nog ' + ProgramTimeLeftString + ' van de ' + ProgramDurationString + ' minuten, begon om ' + ProgramTimeStartString + ' eindigt rond ' + ProgramTimeEndString
                elif dateTimeNow > ProgramTimeEndDateTime:
                    ProgramTimingEpgList = ' duurde ' + ProgramDurationString + ' minuten'
                    ProgramTimingDescription = ' duurde ' + ProgramDurationString + ' minuten, begon om ' + ProgramTimeStartString
                else:
                    ProgramTimingEpgList = ' duurt ' + ProgramDurationString + ' minuten'
                    ProgramTimingDescription = ' duurt ' + ProgramDurationString + ' minuten, eindigt rond ' + ProgramTimeEndString

                #Check if program has active alarm
                if alarm.alarm_duplicate_program_check(ProgramTimeStartDateTime, ChannelId) == True:
                    ProgramAlarm = 'true'
                else:
                    ProgramAlarm = 'false'

                #Check if program is recording event and if the recording is planned or done
                recordProgramEvent = func.search_programid_jsonrecording_event(ProgramId)
                if recordProgramEvent:
                    if dateTimeNow > ProgramTimeEndDateTime:
                        ProgramRecordEventPlanned = 'false'
                        ProgramRecordEventDone = 'true'
                    else:
                        ProgramRecordEventPlanned = 'true'
                        ProgramRecordEventDone = 'false'
                    ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
                    ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent))
                else:
                    ProgramRecordEventPlanned = 'false'
                    ProgramRecordEventDone = 'false'
                    ProgramRecordEventId = ''
                    ProgramStartDeltaTime = '0'

                #Check if program is recording series
                recordProgramSeries = func.search_seriesid_jsonrecording_series(ProgramRecordSeriesId)
                if recordProgramSeries:
                    ProgramRecordSeries = 'true'
                else:
                    ProgramRecordSeries = 'false'

                #Combine the program description
                ProgramEpgList = ProgramTimeStartString + ProgramTimingEpgList
                ProgramDescription = '[COLOR white]' + ProgramName + ProgramTimingDescription + '[/COLOR]\n\n[COLOR gray]' + ProgramDetailsProp + '[/COLOR]\n\n[COLOR white]' + ProgramDescriptionRaw + '[/COLOR]'

                #Update program list item
                updateItem.setProperty('ProgramEpgList', ProgramEpgList)
                updateItem.setProperty('ProgramDescription', ProgramDescription)
                updateItem.setProperty('ProgramAlarm', ProgramAlarm)
                updateItem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
                updateItem.setProperty('ProgramRecordEventPlanned', ProgramRecordEventPlanned)
                updateItem.setProperty('ProgramRecordEventDone', ProgramRecordEventDone)
                updateItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
                updateItem.setProperty('ProgramRecordSeries', ProgramRecordSeries)
                updateItem.setProperty('ProgramProgressPercent', str(ProgramProgressPercent))
            except:
                pass

        #Update the selected channel alarm icon
        self.update_channel_alarm_icon(ChannelId)

        #Update the selected channel recording event icon
        self.update_channel_record_event_icon(ChannelId)

        #Update the selected channel recording series icon
        self.update_channel_record_series_icon(ChannelId)

    def load_epg(self, forceUpdate=False):
        #Check if channel has changed
        epgChannelChanged = self.EpgPreviousChannelId != self.EpgCurrentChannelId

        #Check if the day has changed
        dateTimeNow = datetime.now()
        dateTimeNowString = dateTimeNow.strftime('%Y-%m-%d')
        epgDayString = (dateTimeNow + timedelta(days=self.EpgCurrentLoadDayInt)).strftime('%Y-%m-%d')
        epgDayChanged = self.EpgPreviousLoadDayInt != self.EpgCurrentLoadDayInt
        epgDayTimeChanged = self.EpgPreviousLoadDateTime != dateTimeNowString

        #Check if update is needed
        if forceUpdate or epgChannelChanged or epgDayChanged or epgDayTimeChanged:
            #Get and check the list container
            listcontainer = self.getControl(1002)

            #Clear the current epg items
            listcontainer.reset()

            #Download the epg day information
            func.updateLabelText(self, 1, 'Gids download')
            func.updateLabelText(self, 2, 'TV Gids wordt gedownload, nog even geduld...')
            self.EpgCurrentDayJson = download.download_epg_day(epgDayString, forceUpdate)
            if self.EpgCurrentDayJson == None:
                func.updateLabelText(self, 1, 'Niet beschikbaar')
                func.updateLabelText(self, 2, 'TV Gids is niet beschikbaar.')
                listcontainer = self.getControl(1000)
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
                return
        else:
            #Load program progress
            self.load_progress()

            #Update the status
            self.count_epg(self.EpgCurrentChannelName)
            return

        #Update epg status
        func.updateLabelText(self, 1, 'Gids laden')
        func.updateLabelText(self, 2, 'TV Gids wordt geladen, nog even geduld...')

        ChannelEpg = func.search_channelid_jsonepg(self.EpgCurrentDayJson, self.EpgCurrentChannelId)
        if ChannelEpg == None:
            func.updateLabelText(self, 1, 'Zender gids mist')
            func.updateLabelText(self, 2, 'Gids is niet beschikbaar voor ' + self.EpgCurrentChannelName + '.')
            return

        programSelectIndex = 0
        programCurrentIndex = 0
        for program in ChannelEpg['containers']:
            try:
                #Load program basics
                ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
                ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
                ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(program)

                #Check if program is starting or ending on target day
                ProgramTimeStartDayString = ProgramTimeStartDateTime.strftime('%Y-%m-%d')
                ProgramTimeEndDayString = ProgramTimeEndDateTime.strftime('%Y-%m-%d')
                if ProgramTimeStartDayString != epgDayString and ProgramTimeEndDayString != epgDayString: continue

                #Load program details
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)
                ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))
                ProgramDurationString = metadatainfo.programdurationstring_from_json_metadata(program, False, False)
                EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True, ProgramName)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
                ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(program)
                ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)
                ProgramGenres = metadatainfo.programgenres_from_json_metadata(program)
                ProgramDescriptionRaw = metadatainfo.programdescription_from_json_metadata(program)
                ProgramDescription = 'Programmabeschrijving wordt geladen.'
                ProgramEpgList = 'Programmaduur wordt geladen'

                #Combine program details
                stringJoin = [ EpisodeTitle, ProgramYear, ProgramSeason, ProgramEpisode, ProgramStarRating, ProgramAgeRating, ProgramGenres ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = 'Onbekend seizoen en aflevering'

                #Check if program vod is available for playback
                contentOptionsArray = metadatainfo.contentOptions_from_json_metadata(program)
                if 'CATCHUP' in contentOptionsArray:
                    ProgramAvailable = 'true'
                else:
                    ProgramAvailable = 'false'

                #Check if the program is part of series
                ProgramRecordSeriesId = metadatainfo.seriesId_from_json_metadata(program)

                #Check if current program is a rerun
                programRerunName = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramName.lower())
                programRerunDescription = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramDescription.lower())
                if programRerunName or programRerunDescription:
                    ProgramRerun = 'true'
                else:
                    ProgramRerun = 'false'

                #Add program to the list container
                listitem = xbmcgui.ListItem()
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty('AssetId', self.EpgCurrentAssetId)
                listitem.setProperty('ChannelId', self.EpgCurrentChannelId)
                listitem.setProperty('ExternalId', self.EpgCurrentExternalId)
                listitem.setProperty('ChannelName', self.EpgCurrentChannelName)
                listitem.setProperty('ProgramName', ProgramName)
                listitem.setProperty('ProgramRerun', ProgramRerun)
                listitem.setProperty('ProgramDuration', ProgramDurationString)
                listitem.setProperty('ProgramRecordSeriesId', ProgramRecordSeriesId)
                listitem.setProperty('ProgramDescriptionRaw', ProgramDescriptionRaw)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setProperty('ProgramEpgList', ProgramEpgList)
                listitem.setProperty('ProgramDetails', ProgramDetails)
                listitem.setProperty('ProgramTimeStart', str(ProgramTimeStartDateTime))
                listitem.setProperty('ProgramTimeEnd', str(ProgramTimeEndDateTime))
                listitem.setInfo('video', {'Genre': 'TV Gids', 'Plot': ProgramDescriptionRaw})
                listitem.setArt({'thumb': path.icon_television(self.EpgCurrentExternalId), 'icon': path.icon_television(self.EpgCurrentExternalId)})

                #Check if program finished airing
                if ProgramProgressPercent >= 100:
                    listitem.setProperty('ProgramAvailable', ProgramAvailable)

                #Check if program is still airing
                if ProgramProgressPercent > 0 and ProgramProgressPercent < 100:
                    programSelectIndex = programCurrentIndex

                programCurrentIndex += 1
                listcontainer.addItem(listitem)
            except:
                continue

        #Select program list item
        listcontainer.selectItem(programSelectIndex)
        xbmc.sleep(100)

        #Load program progress
        self.load_progress()

        #Update epg variables
        self.EpgPreviousChannelId = self.EpgCurrentChannelId
        self.EpgPreviousLoadDayInt = self.EpgCurrentLoadDayInt
        self.EpgPreviousLoadDateTime = dateTimeNowString

        #Update the status
        self.count_epg(self.EpgCurrentChannelName)

    #Update the status
    def count_epg(self, ChannelName):
        #Set the epg day string
        epgLoadDayString = self.string_day_number(self.EpgCurrentLoadDayInt)

        #Update the label texts
        listcontainer = self.getControl(1002)
        if listcontainer.size() == 0:
            func.updateLabelText(self, 1, "Geen programma's")
            func.updateLabelText(self, 2, "Geen programma's beschikbaar voor " + epgLoadDayString + " op " + ChannelName + '.')
        else:
            func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's")
            func.updateLabelText(self, 2, "Alle programma's voor " + epgLoadDayString + " op " + ChannelName + '.')

    def thread_update_epg_progress(self):
        threadLastTime = (datetime.now() - timedelta(minutes=1)).strftime('%H:%M')
        while var.thread_update_epg_progress != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime:
                threadLastTime = threadCurrentTime
                self.load_epg()
            else:
                xbmc.sleep(1000)
