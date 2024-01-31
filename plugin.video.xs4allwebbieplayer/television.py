from datetime import datetime, timedelta
import xbmc
import xbmcgui
import alarm
import lichanneltelevision
import dialog
import download
import epg
import favorite
import hidden
import func
import lifunc
import path
import litelevision
import recordingfunc
import searchdialog
import streamplay
import var
import zap

def switch_to_page():
    if var.guiTelevision == None:
        channelView = var.addon.getSetting('TelevisionChannelView').lower()
        if channelView == 'lijst':
            var.guiTelevision = Gui('television.xml', var.addonpath, 'default', '720p')
        elif channelView == 'blokken':
            var.guiTelevision = Gui('television-grid.xml', var.addonpath, 'default', '720p')
        elif channelView == 'minimaal':
            var.guiTelevision = Gui('television-min.xml', var.addonpath, 'default', '720p')
        var.guiTelevision.show()

def close_the_page():
    if var.guiTelevision != None:
        #Stop the epg refresh thread
        var.thread_update_television_program.Stop()

        #Close the shown window
        var.guiTelevision.close()
        var.guiTelevision = None

def source_plugin_list():
    download.download_channels_tv(False)
    lichanneltelevision.list_load(None)

class Gui(xbmcgui.WindowXML):
    EpgPauseUpdate = False
    EpgForceUpdate = False
    EpgManualUpdate = False

    def onInit(self):
        self.buttons_add_navigation()
        self.load_recording_event(False)
        self.load_recording_series(False)
        self.load_channels(False, False)
        self.start_threads()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer.Finished():
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'play_stream_tv':
                    streamplay.play_tv(listItemSelected)
            elif clickId == 1001:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'go_back':
                    close_the_page()
                elif listItemAction == 'refresh_programs':
                    self.refresh_programs(True)
                elif listItemAction == 'hidden_channels':
                    hidden.switch_to_page()
                elif listItemAction == "switch_all_favorites":
                    self.switch_all_favorites()
                elif listItemAction == "search_channel":
                    self.search_channel()
            elif clickId == 9000:
                if xbmc.Player().isPlayingVideo():
                    var.PlayerCustom.Fullscreen(True)
                else:
                    listContainer = self.getControl(1001)
                    self.setFocus(listContainer)
                    xbmc.sleep(100)
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
        self.EpgForceUpdate = False

        #Start the epg update thread
        var.thread_update_television_program.Start(self.thread_update_television_program)

    def open_context_menu(self):
        dialogAnswers = []
        dialogHeader = 'Televisie Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde zender?'
        dialogFooter = ''

        #Get the selected channel
        listContainer = self.getControl(1000)
        listItemSelected = listContainer.getSelectedItem()

        #Add watch program from beginning
        dialogAnswers.append('Programma vanaf begin kijken')
        dialogAnswers.append('Programma in de TV Gids tonen')

        #Add record program
        if var.RecordingAccess() == True:
            dialogAnswers.append('Huidig programma opnemen of annuleren')
            dialogAnswers.append('Volgend programma opnemen of annuleren')
            dialogAnswers.append('Huidig serie seizoen opnemen of annuleren')

        #Add set alarm for next program
        dialogAnswers.append('Alarm volgend programma zetten of annuleren')

        #Add hide channel
        dialogAnswers.append('Zender verbergen in zenderlijst')

        #Check if channel is favorite
        if listItemSelected.getProperty('ChannelFavorite') == 'true':
            dialogAnswers.append('Zender onmarkeren als favoriet')
        else:
            dialogAnswers.append('Zender markeren als favoriet')

        #Add switch favorite/all button
        if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
            dialogAnswers.append('Toon alle zenders')
        else:
            dialogAnswers.append('Toon favorieten zenders')

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma vanaf begin kijken':
            ProgramTimeStartProp = listItemSelected.getProperty('ProgramNowTimeStartDateTime')
            ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartProp, '%Y-%m-%d %H:%M:%S')
            ProgramTimeStartOffset = int((datetime.now() - ProgramTimeStartDateTime).total_seconds())
            streamplay.play_tv(listItemSelected, SeekOffsetEnd=ProgramTimeStartOffset)
        elif dialogResult == 'Programma in de TV Gids tonen':
            var.EpgNavigateProgramId = listItemSelected.getProperty("ProgramNowId")
            var.EpgCurrentChannelId = listItemSelected.getProperty("ChannelId")
            var.EpgCurrentLoadDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramNowTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
            close_the_page()
            xbmc.sleep(100)
            epg.switch_to_page()
        elif dialogResult == 'Zender verbergen in zenderlijst':
            self.hide_channel(listContainer, listItemSelected)
        elif dialogResult == 'Zender markeren als favoriet' or dialogResult == 'Zender onmarkeren als favoriet':
            self.switch_favorite_channel(listContainer, listItemSelected)
        elif dialogResult == 'Huidig programma opnemen of annuleren':
            recordingfunc.record_event_now_television_playergui(listItemSelected)
        elif dialogResult == 'Volgend programma opnemen of annuleren':
            recordingfunc.record_event_next_television_playergui(listItemSelected)
        elif dialogResult == 'Huidig serie seizoen opnemen of annuleren':
            recordingfunc.record_series_television_playergui(listItemSelected)
        elif dialogResult == 'Alarm volgend programma zetten of annuleren':
            self.set_program_alarm_next(listItemSelected)
        elif dialogResult == 'Toon alle zenders' or dialogResult == 'Toon favorieten zenders':
            self.switch_all_favorites()

    def set_program_alarm_next(self, listItemSelected):
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
        listItem.setProperty('Action', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Alle of favorieten')
        listItem.setProperty('Action', 'switch_all_favorites')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/star.png'), 'icon': path.resources('resources/skins/default/media/common/star.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek naar zender')
        listItem.setProperty('Action', 'search_channel')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Verborgen zenders')
        listItem.setProperty('Action', 'hidden_channels')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/vodno.png'), 'icon': path.resources('resources/skins/default/media/common/vodno.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Vernieuwen')
        listItem.setProperty('Action', 'refresh_programs')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listContainer.addItem(listItem)

    def refresh_programs(self, forceUpdate=False):
        try:
            self.load_recording_event(forceUpdate)
            self.load_recording_series(forceUpdate)
            self.load_channels(True, forceUpdate)
        except:
            pass

    def hide_channel(self, listContainer, listItemSelected):
        self.EpgPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.hide_channel_code(listContainer, listItemSelected)
        self.EpgPauseUpdate = False

    def hide_channel_code(self, listContainer, listItemSelected):
        hiddenResult = hidden.hidden_add(listItemSelected, 'HiddenTelevision.js')
        if hiddenResult == True:
            #Remove item from the list
            removeListItemId = listContainer.getSelectedPosition()
            listContainer.removeItem(removeListItemId)
            xbmc.sleep(100)
            listContainer.selectItem(removeListItemId)
            xbmc.sleep(100)

            #Update the status
            self.count_channels(False)

    def switch_favorite_channel(self, listContainer, listItemSelected):
        self.EpgPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.switch_favorite_channel_code(listContainer, listItemSelected)
        self.EpgPauseUpdate = False

    def switch_favorite_channel_code(self, listContainer, listItemSelected):
        favoriteResult = favorite.favorite_toggle(listItemSelected, 'FavoriteTelevision.js')
        if favoriteResult == 'Removed' and var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
            #Remove item from the list
            removeListItemId = listContainer.getSelectedPosition()
            listContainer.removeItem(removeListItemId)
            xbmc.sleep(100)
            listContainer.selectItem(removeListItemId)
            xbmc.sleep(100)

            #Update the status
            self.count_channels(False)

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

            #Load television channels
            self.load_channels(True, False)
        except:
            pass

    def search_channel(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistoryChannel.js', 'Zoek naar zender')

        #Check if search cancelled
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchChannelTerm = func.search_filter_string(searchDialogTerm.string)

        #Load television channels
        self.load_channels(True, False)

        #Reset search variable
        var.SearchChannelTerm = ''

    def load_recording_event(self, forceUpdate=False):
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False: return False

    def load_recording_series(self, forceUpdate=False):
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False: return False

    def load_channels(self, forceLoad=False, forceUpdate=False):
        self.EpgPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.load_channels_code(forceLoad, forceUpdate)
        self.EpgPauseUpdate = False

    def load_channels_code(self, forceLoad=False, forceUpdate=False):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Zenders worden vernieuwd.', notificationIcon, 2500, False)

        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listContainer.size() > 0:
                currentChannelId = var.addon.getSetting('CurrentChannelId')
                lifunc.focus_on_channelid_in_list(self, 1000, 0, True, currentChannelId)
                return True
        else:
            listContainer.reset()

        #Download the channels
        func.updateLabelText(self, 1, 'Zenders downloaden')
        downloadResult = download.download_channels_tv(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            listContainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, 'Zenders laden')

        #Add items to sort list
        listContainerSort = []
        lichanneltelevision.list_load(listContainerSort)

        #Sort and add items to container
        listContainer.addItems(listContainerSort)

        #Update the status
        self.count_channels(True)

        #Force manual epg update
        self.EpgManualUpdate = True
        self.EpgForceUpdate = forceUpdate

    #Update the status
    def count_channels(self, resetSelect=False):
        #Set channel type string
        channelTypeString = 'zenders'
        if var.addon.getSetting('LoadChannelFavoritesOnly') == 'true':
            channelTypeString = 'favorieten zenders'

        #Update status label text
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, str(listContainer.size()) + ' zenders gevonden')
                func.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
            else:
                func.updateLabelText(self, 1, str(listContainer.size()) + ' ' + channelTypeString)
                if var.ApiHomeAccess() == True:
                    func.updateLabelText(self, 3, "")
                else:
                    func.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")

            if resetSelect == True:
                currentChannelId = var.addon.getSetting('CurrentChannelId')
                lifunc.focus_on_channelid_in_list(self, 1000, 0, True, currentChannelId)
        else:
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                func.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
                listContainer.selectItem(2)
            else:
                func.updateLabelText(self, 1, 'Geen ' + channelTypeString)
                if var.ApiHomeAccess() == True:
                    func.updateLabelText(self, 3, "")
                else:
                    func.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")
                listContainer.selectItem(0)
            xbmc.sleep(100)

    def thread_update_television_program(self):
        threadLastTime = ''
        while var.thread_update_television_program.Allowed():
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime or self.EpgManualUpdate or self.EpgForceUpdate:
                threadLastTime = threadCurrentTime
                forceUpdate = self.EpgForceUpdate

                #Reset update variables
                self.EpgManualUpdate = False
                self.EpgForceUpdate = False

                #Update program information
                self.update_television_program(forceUpdate)
            else:
                var.thread_update_television_program.Sleep(1000)

    def update_television_program(self, forceUpdate=False):
        try:
            if forceUpdate == True:
                #Show tv guide refresh notification
                notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
                xbmcgui.Dialog().notification(var.addonname, 'TV Gids wordt vernieuwd.', notificationIcon, 2500, False)

                #Download epg information for today
                download.download_epg_day(datetime.now(), True)

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
