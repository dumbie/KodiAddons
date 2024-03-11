from datetime import datetime, timedelta
import xbmc
import xbmcgui
import alarm
import dialog
import epg
import favorite
import func
import getset
import guifunc
import hidden
import lichanneltelevision
import lifunc
import litelevision
import path
import player
import recordingfunc
import search
import searchdialog
import streamplay
import var
import zap

def switch_to_page():
    if var.guiTelevision == None:
        channelView = getset.setting_get('TelevisionChannelView').lower()
        if channelView == 'lijst':
            var.guiTelevision = Gui('television.xml', var.addonpath, 'default', '720p')
        elif channelView == 'blokken':
            var.guiTelevision = Gui('television-grid.xml', var.addonpath, 'default', '720p')
        elif channelView == 'minimaal':
            var.guiTelevision = Gui('television-min.xml', var.addonpath, 'default', '720p')
        var.guiTelevision.setProperty('WebbiePlayerPage', 'Open')
        var.guiTelevision.show()

def close_the_page():
    if var.guiTelevision != None:
        #Stop the epg refresh thread
        var.thread_update_television_program.Stop()

        #Close the shown window
        var.guiTelevision.close()
        var.guiTelevision = None

class Gui(xbmcgui.WindowXML):
    EpgPauseUpdate = False
    EpgManualUpdate = False

    def onInit(self):
        self.buttons_add_navigation()
        self.load_channels(False)
        self.start_threads()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer.Finished():
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('ItemAction')
                if listItemAction == 'play_stream_tv':
                    streamplay.play_tv(listItemSelected)
            elif clickId == 1001:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('ItemAction')
                if listItemAction == 'go_back':
                    close_the_page()
                elif listItemAction == 'hidden_channels':
                    hidden.switch_to_page()
                elif listItemAction == "switch_all_favorites":
                    self.switch_all_favorites()
                elif listItemAction == "search_channel":
                    self.search_channel()
            elif clickId == 9000:
                if xbmc.Player().isPlaying():
                    player.Fullscreen(True)
                else:
                    listContainer = self.getControl(1001)
                    guifunc.controlFocus(self, listContainer)
            elif clickId == 3001:
                close_the_page()

    def onAction(self, action):
        actionId = action.getId()
        focusChannel = xbmc.getCondVisibility('Control.HasFocus(1000)')
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')
        elif actionId == var.ACTION_PLAYER_PLAY:
            self.switch_all_favorites()
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_channel()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusChannel:
            self.open_context_menu()
        else:
            zap.check_remote_number(self, 1000, actionId, True, False)

    def start_threads(self):
        #Force manual epg update
        self.EpgManualUpdate = True

        #Start the epg update thread
        var.thread_update_television_program.Start(self.thread_update_television_program)

    def open_context_menu(self):
        dialogAnswers = []
        dialogHeader = 'Zender Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde zender?'
        dialogFooter = ''

        #Get the selected channel
        listContainer = self.getControl(1000)
        listItemSelected = listContainer.getSelectedItem()

        #Add watch program from beginning
        dialogAnswers.append('Programma vanaf begin kijken')
        dialogAnswers.append('Programma in de TV Gids tonen')
        dialogAnswers.append('Programma uitzendingen terugzoeken')

        #Add record program
        if var.RecordingAccess() == True:
            dialogAnswers.append('Huidig programma opnemen of annuleren')
            dialogAnswers.append('Huidig serie seizoen opnemen of annuleren')
            dialogAnswers.append('Volgend programma opnemen of annuleren')
            dialogAnswers.append('Volgend serie seizoen opnemen of annuleren')

        #Add set alarm for next program
        dialogAnswers.append('Volgend programma alarm zetten of annuleren')

        #Add hide channel
        dialogAnswers.append('Zender verbergen in zenderlijst')

        #Check if channel is favorite
        if listItemSelected.getProperty('ChannelFavorite') == 'true':
            dialogAnswers.append('Zender onmarkeren als favoriet')
        else:
            dialogAnswers.append('Zender markeren als favoriet')

        #Add switch favorite/all button
        if getset.setting_get('LoadChannelFavoritesOnly') == 'true':
            dialogAnswers.append('Toon alle zenders')
        else:
            dialogAnswers.append('Toon favorieten zenders')

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma vanaf begin kijken':
            self.program_watch_beginning(listItemSelected)
        elif dialogResult == 'Programma in de TV Gids tonen':
            self.program_show_in_epg(listItemSelected)
        elif dialogResult == 'Programma uitzendingen terugzoeken':
            self.search_program_history(listItemSelected)
        elif dialogResult == 'Zender verbergen in zenderlijst':
            self.hide_channel(listContainer, listItemSelected)
        elif dialogResult == 'Zender markeren als favoriet' or dialogResult == 'Zender onmarkeren als favoriet':
            self.switch_favorite_channel(listContainer, listItemSelected)
        elif dialogResult == 'Huidig programma opnemen of annuleren':
            recordingfunc.record_event_now_television_playergui(listItemSelected)
        elif dialogResult == 'Huidig serie seizoen opnemen of annuleren':
            recordingfunc.record_series_now_television_playergui(listItemSelected)
        elif dialogResult == 'Volgend programma opnemen of annuleren':
            recordingfunc.record_event_next_television_playergui(listItemSelected)
        elif dialogResult == 'Volgend serie seizoen opnemen of annuleren':
            recordingfunc.record_series_next_television_playergui(listItemSelected)
        elif dialogResult == 'Volgend programma alarm zetten of annuleren':
            self.program_alarm_set_next(listItemSelected)
        elif dialogResult == 'Toon alle zenders' or dialogResult == 'Toon favorieten zenders':
            self.switch_all_favorites()

    def program_watch_beginning(self, listItemSelected):
        ProgramTimeStart = listItemSelected.getProperty('ProgramNowTimeStartDateTime')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStart, '%Y-%m-%d %H:%M:%S')
        SeekOffsetSecEnd = int((datetime.now() - ProgramTimeStartDateTime).total_seconds())
        streamplay.play_tv(listItemSelected, SeekOffsetSecEnd=SeekOffsetSecEnd)
    
    def program_show_in_epg(self, listItemSelected):
        var.EpgNavigateProgramId = listItemSelected.getProperty("ProgramNowId")
        var.EpgCurrentChannelId = listItemSelected.getProperty("ChannelId")
        var.EpgCurrentLoadDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramNowTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
        close_the_page()
        epg.switch_to_page()

    def search_program_history(self, listItemSelected):
        ProgramName = listItemSelected.getProperty("ProgramNowName")
        if var.SearchTermDownload != ProgramName:
            var.SearchSelectIdentifier = ''
            var.SearchTermResult = ''
            var.SearchTermDownload = ProgramName
            var.SearchProgramDataJson = []
        close_the_page()
        search.switch_to_page()

    def program_alarm_set_next(self, listItemSelected):
        ExternalId = listItemSelected.getProperty("ExternalId")
        ChannelId = listItemSelected.getProperty("ChannelId")
        ChannelName = listItemSelected.getProperty("ChannelName")
        ProgramNextName = listItemSelected.getProperty("ProgramNextNameRaw")
        ProgramNextTimeStartDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramNextTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')

        #Check the next program time
        if ProgramNextTimeStartDateTime != datetime(1970,1,1):
            #Set or remove the next program alarm
            alarmAdded = alarm.alarm_add(ProgramNextTimeStartDateTime, ChannelId, ExternalId, ChannelName, ProgramNextName, True)

            #Update alarm icon in the information
            if alarmAdded == True:
                listItemSelected.setProperty("ProgramNextAlarm", 'true')
            elif alarmAdded == 'Remove':
                listItemSelected.setProperty("ProgramNextAlarm", 'false')

    def buttons_add_navigation(self):
        listContainer = self.getControl(1001)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga een stap terug')
        listItem.setProperty('ItemAction', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek naar zender')
        listItem.setProperty('ItemAction', 'search_channel')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Alle of favorieten')
        listItem.setProperty('ItemAction', 'switch_all_favorites')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/star.png'), 'icon': path.resources('resources/skins/default/media/common/star.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Verborgen zenders')
        listItem.setProperty('ItemAction', 'hidden_channels')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/vodno.png'), 'icon': path.resources('resources/skins/default/media/common/vodno.png')})
        listContainer.addItem(listItem)

    def hide_channel(self, listContainer, listItemSelected):
        self.EpgPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.hide_channel_code(listContainer, listItemSelected)
        self.EpgPauseUpdate = False

    def hide_channel_code(self, listContainer, listItemSelected):
        hiddenResult = hidden.hidden_add(listItemSelected, 'HiddenTelevision.js')
        if hiddenResult == True:
            #Remove item from the list
            removeListItemIndex = listContainer.getSelectedPosition()
            guifunc.listRemoveItem(listContainer, removeListItemIndex)
            guifunc.listSelectIndex(listContainer, removeListItemIndex)

            #Update the status
            self.count_channels(False)

    def switch_favorite_channel(self, listContainer, listItemSelected):
        self.EpgPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.switch_favorite_channel_code(listContainer, listItemSelected)
        self.EpgPauseUpdate = False

    def switch_favorite_channel_code(self, listContainer, listItemSelected):
        favoriteResult = favorite.favorite_toggle_channel(listItemSelected, 'FavoriteTelevision.js')
        if favoriteResult == 'Removed' and getset.setting_get('LoadChannelFavoritesOnly') == 'true':
            #Remove item from the list
            removeListItemIndex = listContainer.getSelectedPosition()
            guifunc.listRemoveItem(listContainer, removeListItemIndex)
            guifunc.listSelectIndex(listContainer, removeListItemIndex)

            #Update the status
            self.count_channels(False)

    def switch_all_favorites(self):
        try:
            #Switch favorites mode on or off
            if favorite.favorite_switch_mode('FavoriteTelevision.js') == False:
                return

            #Load television channels
            self.load_channels(True)
        except:
            pass

    def search_channel(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistoryChannel.js', 'Zoek naar zender')

        #Check if search cancelled
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchTermResult = func.search_filter_string(searchDialogTerm.string)
        self.load_channels(True)
        var.SearchTermResult = ''

    def load_channels(self, forceLoad=False):
        self.EpgPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.load_channels_code(forceLoad)
        self.EpgPauseUpdate = False

    def load_channels_code(self, forceLoad=False):
        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False:
            if listContainer.size() > 0:
                currentChannelId = getset.setting_get('CurrentChannelId', True)
                lifunc.focus_listcontainer_value(self, 1000, 0, True, 'ChannelId', currentChannelId)
                return True
        else:
            guifunc.listReset(listContainer)

        #Add items to list container
        guifunc.updateLabelText(self, 1, 'Zenders laden')
        guifunc.updateLabelText(self, 3, "")
        if lichanneltelevision.list_load_combined(listContainer) == False:
            guifunc.updateLabelText(self, 1, 'Niet beschikbaar')
            guifunc.updateLabelText(self, 3, "")
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectIndex(listContainer, 0)
            return False

        #Update the status
        self.count_channels(True)

        #Force manual epg update
        self.EpgManualUpdate = True

    #Update the status
    def count_channels(self, resetSelect=False):
        #Set channel type string
        channelTypeString = 'zenders'
        if getset.setting_get('LoadChannelFavoritesOnly') == 'true':
            channelTypeString = 'favorieten zenders'

        #Update status label text
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + ' zenders gevonden')
                guifunc.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchTermResult)
            else:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + ' ' + channelTypeString)
                if var.ApiHomeAccess() == True:
                    guifunc.updateLabelText(self, 3, "")
                else:
                    guifunc.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")

            if resetSelect == True:
                currentChannelId = getset.setting_get('CurrentChannelId', True)
                lifunc.focus_listcontainer_value(self, 1000, 0, True, 'ChannelId', currentChannelId)
        else:
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.updateLabelText(self, 1, 'Geen zenders gevonden')
                guifunc.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchTermResult)
                guifunc.listSelectIndex(listContainer, 2)
            else:
                guifunc.updateLabelText(self, 1, 'Geen ' + channelTypeString)
                if var.ApiHomeAccess() == True:
                    guifunc.updateLabelText(self, 3, "")
                else:
                    guifunc.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")
                guifunc.listSelectIndex(listContainer, 0)

    def thread_update_television_program(self):
        threadLastTime = ''
        while var.thread_update_television_program.Allowed(sleepDelayMs=1000):
            try:
                threadCurrentTime = datetime.now().strftime('%H:%M')
                if threadLastTime != threadCurrentTime or self.EpgManualUpdate == True:
                    #Update thread variables
                    threadLastTime = threadCurrentTime
                    self.EpgManualUpdate = False

                    #Update program information
                    self.update_television_program()
            except:
                pass

    def update_television_program(self):
        try:
            #Get and check the list container
            listContainer = self.getControl(1000)
            listItemCount = listContainer.size()

            #Generate program summary for television
            for itemNum in range(0, listItemCount):
                try:
                    #Check if epg is allowed to update
                    if self.EpgPauseUpdate: return

                    #Generate and update program summary
                    updateItem = listContainer.getListItem(itemNum)
                    litelevision.list_update(updateItem)
                except:
                    continue
        except:
            pass
