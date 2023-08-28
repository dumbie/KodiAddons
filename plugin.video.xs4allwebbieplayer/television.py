from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import alarm
import channel.television
import dialog
import download
import epg
import favorite
import func
import path
import program.television
import recordingfunc
import searchdialog
import stream
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
        var.thread_update_television_epg = None

        #Close the shown window
        var.guiTelevision.close()
        var.guiTelevision = None

class Gui(xbmcgui.WindowXML):
    EpgIsUpdating = False
    EpgForceUpdate = False

    def onInit(self):
        self.buttons_add_navigation()
        favorite.favorite_json_load()
        self.load_channels(False, False)
        self.load_recording_event(False)
        self.load_recording_series(False)

        #Force an epg update
        self.EpgForceUpdate = True

        #Start the epg update thread
        if var.thread_update_television_epg == None:
            var.thread_update_television_epg = Thread(target=self.thread_update_television_epg)
            var.thread_update_television_epg.start()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer == None:
            clickedControl = self.getControl(clickId)
            if clickId == 1000:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'play_stream':
                    stream.switch_channel_tv_listitem(listItemSelected, False, False)
            elif clickId == 1001:
                listItemSelected = clickedControl.getSelectedItem()
                listItemAction = listItemSelected.getProperty('Action')
                if listItemAction == 'go_back':
                    close_the_page()
                elif listItemAction == 'refresh_programs':
                    self.refresh_programs()
                elif listItemAction == "switch_allfavorites":
                    self.switch_allfavorites()
                elif listItemAction == "search_channelprogram":
                    self.search_channelprogram()
            elif clickId == 9000:
                if xbmc.Player().isPlayingVideo():
                    var.PlayerCustom.Fullscreen(True)
                else:
                    listcontainer = self.getControl(1001)
                    self.setFocus(listcontainer)
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
            self.switch_allfavorites()
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_channelprogram()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusChannel:
            self.open_context_menu()
        else:
            zap.check_remote_number(self, 1000, actionId, True, False)

    def open_context_menu(self):
        dialogAnswers = []
        dialogHeader = 'Televisie Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde zender?'
        dialogFooter = ''

        #Get the selected channel
        listcontainer = self.getControl(1000)
        listItemSelected = listcontainer.getSelectedItem()

        #Add watch program from beginning
        dialogAnswers.append('Programma vanaf begin kijken')
        dialogAnswers.append('Programma in de TV Gids tonen')

        #Check if channel is favorite
        if listItemSelected.getProperty('ChannelFavorite') == 'true':
            dialogAnswers.append('Zender onmarkeren als favoriet')
        else:
            dialogAnswers.append('Zender markeren als favoriet')

        #Add record program
        if var.RecordingAccess == True:
            dialogAnswers.append('Huidig programma opnemen of annuleren')
            dialogAnswers.append('Volgend programma opnemen of annuleren')
            dialogAnswers.append('Huidig serie seizoen opnemen of annuleren')

        #Add set alarm for next program
        dialogAnswers.append('Alarm volgend programma zetten of annuleren')

        #Add switch favorite/all button
        if var.LoadChannelFavoritesOnly == True:
            dialogAnswers.append('Toon alle zenders')
        else:
            dialogAnswers.append('Toon favorieten zenders')

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma vanaf begin kijken':
            ProgramTimeStartProp = listItemSelected.getProperty('ProgramNowTimeStartDateTime')
            ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartProp, '%Y-%m-%d %H:%M:%S')
            ProgramTimeStartOffset = int((datetime.now() - ProgramTimeStartDateTime).total_seconds())
            stream.switch_channel_tv_listitem(listItemSelected, False, False, ProgramTimeStartOffset)
        elif dialogResult == 'Programma in de TV Gids tonen':
            var.EpgNavigateProgramId = listItemSelected.getProperty("ProgramNowId")
            var.EpgCurrentChannelId = listItemSelected.getProperty("ChannelId")
            var.EpgCurrentLoadDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramNowTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
            close_the_page()
            xbmc.sleep(100)
            epg.switch_to_page()

        elif dialogResult == 'Zender markeren als favoriet' or dialogResult == 'Zender onmarkeren als favoriet':
            favoriteRemoved = favorite.favorite_add(listItemSelected)
            if favoriteRemoved == 'Removed' and var.LoadChannelFavoritesOnly == True:
                #Remove item from the list
                removeListItemId = listcontainer.getSelectedPosition()
                listcontainer.removeItem(removeListItemId)
                xbmc.sleep(100)
                listcontainer.selectItem(removeListItemId)
                xbmc.sleep(100)

                #Update the status
                self.count_channels(False)
        elif dialogResult == 'Huidig programma opnemen of annuleren':
            recordingfunc.record_event_now_television_playergui(listItemSelected)
        elif dialogResult == 'Volgend programma opnemen of annuleren':
            recordingfunc.record_event_next_television_playergui(listItemSelected)
        elif dialogResult == 'Huidig serie seizoen opnemen of annuleren':
            recordingfunc.record_series_television_playergui(listItemSelected)
        elif dialogResult == 'Alarm volgend programma zetten of annuleren':
            self.set_program_alarm_next(listItemSelected)
        elif dialogResult == 'Toon alle zenders' or dialogResult == 'Toon favorieten zenders':
            self.switch_allfavorites()

    def set_program_alarm_next(self, listItemSelected):
        ExternalId = listItemSelected.getProperty("ExternalId")
        ChannelId = listItemSelected.getProperty("ChannelId")
        ChannelName = listItemSelected.getProperty("ChannelName")
        ProgramNextName = listItemSelected.getProperty("ProgramNextNameRaw")
        ProgramNextTimeStartDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramNextTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')

        #Check the next program time
        if ProgramNextTimeStartDateTime != datetime(1970, 1, 1):
            #Set or remove the next program alarm
            alarmAdded = alarm.alarm_add(ProgramNextTimeStartDateTime, ChannelId, ExternalId, ChannelName, ProgramNextName, True)

            #Update alarm icon in the information
            if alarmAdded == True:
                listItemSelected.setProperty("ProgramNextAlarm", 'true')
            elif alarmAdded == 'Remove':
                listItemSelected.setProperty("ProgramNextAlarm", 'false')

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Alle of favorieten')
        listitem.setProperty('Action', 'switch_allfavorites')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/star.png'), 'icon': path.resources('resources/skins/default/media/common/star.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zoek naar zender')
        listitem.setProperty('Action', 'search_channelprogram')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Vernieuwen')
        listitem.setProperty('Action', 'refresh_programs')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def refresh_programs(self):
        try:
            #Check if television is busy
            if self.EpgIsUpdating == True:
                notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
                xbmcgui.Dialog().notification(var.addonname, 'TV Gids is bezig.', notificationIcon, 2500, False)
                return

            self.load_channels(True, True)
            self.load_recording_event(True)
            self.load_recording_series(True)
            self.load_epg(True)
        except:
            pass

    def switch_allfavorites(self):
        try:
            #Check if television is busy
            if self.EpgIsUpdating == True:
                notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
                xbmcgui.Dialog().notification(var.addonname, 'TV Gids is bezig.', notificationIcon, 2500, False)
                return

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

            self.load_channels(True, False)
            self.load_epg(False)
        except:
            pass

    def search_channelprogram(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek naar zender', True)

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Check if television is busy
        if self.EpgIsUpdating == True:
            notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
            xbmcgui.Dialog().notification(var.addonname, 'TV Gids is bezig.', notificationIcon, 2500, False)
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_channels(True, False)
        self.load_epg(False)
        var.SearchFilterTerm = ''

    def load_recording_event(self, forceUpdate=False):
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False: return False

    def load_recording_series(self, forceUpdate=False):
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False: return False

    def load_channels(self, forceLoad=False, forceUpdate=False):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/television.png')
            xbmcgui.Dialog().notification(var.addonname, 'Zenders worden vernieuwd.', notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0:
                currentChannelId = var.addon.getSetting('CurrentChannelId')
                func.focus_on_channel_list(self, 1000, 0, True, currentChannelId)
                return True
        else:
            listcontainer.reset()

        #Download the channels
        func.updateLabelText(self, 1, 'Zenders downloaden')
        downloadResult = download.download_channels_tv(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Add channels to list
        func.updateLabelText(self, 1, 'Zenders laden')
        channel.television.list_load(listcontainer)

        #Update the status
        self.count_channels(True)

    #Update the status
    def count_channels(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + ' zenders gevonden')
                func.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchFilterTerm)
            elif var.LoadChannelFavoritesOnly == True:
                func.updateLabelText(self, 1, str(listcontainer.size()) + ' favorieten zenders')
                if var.ApiHomeAccess == True:
                    func.updateLabelText(self, 3, "")
                else:
                    func.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + ' zenders')
                if var.ApiHomeAccess == True:
                    func.updateLabelText(self, 3, "")
                else:
                    func.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")

            if resetSelect == True:
                currentChannelId = var.addon.getSetting('CurrentChannelId')
                func.focus_on_channel_list(self, 1000, 0, True, currentChannelId)
        else:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, 'Geen zenders gevonden')
                func.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchFilterTerm)
                listcontainer.selectItem(2)
            elif var.LoadChannelFavoritesOnly == True:
                func.updateLabelText(self, 1, 'Geen favorieten zenders')
                if var.ApiHomeAccess == True:
                    func.updateLabelText(self, 3, "")
                else:
                    func.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen zenders')
                if var.ApiHomeAccess == True:
                    func.updateLabelText(self, 3, "")
                else:
                    func.updateLabelText(self, 3, "Buitenshuis zijn er minder zenders beschikbaar.")
                listcontainer.selectItem(0)
            xbmc.sleep(100)

    def thread_update_television_epg(self):
        threadLastTime = (datetime.now() - timedelta(minutes=1)).strftime('%H:%M')
        while var.thread_update_television_epg != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime or self.EpgForceUpdate:
                threadLastTime = threadCurrentTime
                self.EpgForceUpdate = False
                self.EpgIsUpdating = True
                self.load_epg(False)
                self.EpgIsUpdating = False
            else:
                xbmc.sleep(2000)

    def load_epg(self, forceUpdate=False):
        try:
            if forceUpdate == True:
                #Show tv guide refresh notification
                notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
                xbmcgui.Dialog().notification(var.addonname, 'TV Gids wordt vernieuwd.', notificationIcon, 2500, False)

                #Download epg information for today
                download.download_epg_day(datetime.now(), True)

            #Get and check the list container
            listcontainer = self.getControl(1000)
            listitemcount = listcontainer.size()

            #Generate program summary for television
            for itemNum in range(0, listitemcount):
                try:
                    updateItem = listcontainer.getListItem(itemNum)
                    program.television.list_update(updateItem)
                except:
                    continue
        except:
            pass
