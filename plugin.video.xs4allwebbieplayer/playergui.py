from datetime import datetime, timedelta
import xbmc
import xbmcgui
import alarm
import lichanneltelevision
import func
import lifunc
import path
import liplayergui
import recordingfunc
import sleep
import streamplay
import var
import zap

def switch_to_page():
    if var.guiPlayer == None and var.PlayerGuiOpen() == False:
        #Update open variable
        var.PlayerGuiOpen(True)

        #Show player gui overlay
        var.guiPlayer = Gui('playergui.xml', var.addonpath, 'default', '720p')
        var.guiPlayer.show()

def close_the_page():
    if var.guiPlayer != None:
        #Stop update information thread
        var.thread_update_playergui_info.Stop()

        #Stop hide information thread
        var.thread_hide_playergui_info.Stop()

        #Close custom video player window
        var.guiPlayer.close()
        var.guiPlayer = None
        xbmc.sleep(100)

        #Close fullscreen player window
        func.close_window_id(var.WINDOW_VISUALISATION)
        func.close_window_id(var.WINDOW_FULLSCREEN_VIDEO)
        xbmc.sleep(100)

        #Update open variable
        var.PlayerGuiOpen(False)

class Gui(xbmcgui.WindowXMLDialog):
    EpgPauseUpdate = False
    ChannelDelay = datetime(1970,1,1)
    InfoLastHide = datetime(1970,1,1)
    InfoLastInteraction = datetime(1970,1,1)

    def onInit(self):
        self.buttons_add_sidebar()
        self.load_channels()
        self.start_threads()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer.Finished():
            clickedControl = self.getControl(clickId)
            playerFull = self.getProperty('WebbiePlayerFull') == 'true'
            if clickId == 1001 and playerFull == True:
                listItemClicked = clickedControl.getSelectedItem()
                streamplay.play_tv(listItemClicked, ShowInformation=True)
            elif clickId == 1002 and playerFull == True:
                listItemClicked = clickedControl.getSelectedItem()
                listItemAction = listItemClicked.getProperty('ItemAction')
                if listItemAction == 'media_lastchannel':
                    self.switch_channel_lasttv()
                elif listItemAction == 'media_sleep':
                    sleep.dialog_sleep()
                elif listItemAction == 'media_alarmnext':
                    self.set_alarm_next()
                elif listItemAction == 'media_record_event':
                    listContainer = self.getControl(1001)
                    listItemSelectedChannel = listContainer.getSelectedItem()
                    recordingfunc.record_event_now_television_playergui(listItemSelectedChannel)
                elif listItemAction == 'media_record_series':
                    listContainer = self.getControl(1001)
                    listItemSelectedChannel = listContainer.getSelectedItem()
                    recordingfunc.record_series_television_playergui(listItemSelectedChannel)
                elif listItemAction == 'media_volumeup':
                    self.media_volume_up()
                elif listItemAction == 'media_volumedown':
                    self.media_volume_down()
                elif listItemAction == 'media_togglemute':
                    xbmc.executebuiltin('Action(Mute)')
                elif listItemAction == 'media_subtitlesonoff':
                    self.switch_subtitles()
                elif listItemAction == 'media_seekback':
                    self.seek_back(False)
                elif listItemAction == 'media_seekforward':
                    self.seek_forward(False)
                elif listItemAction == 'media_seeklive':
                    self.seek_live()
                elif listItemAction == 'media_seekbegin':
                    self.seek_begin_program()
                elif listItemAction == 'media_stop':
                    xbmc.executebuiltin('PlayerControl(Stop)')
                elif listItemAction == 'media_playpause':
                    xbmc.executebuiltin('PlayerControl(Play)')
                elif listItemAction == 'media_previousscreen':
                    close_the_page()
                elif listItemAction == 'media_fullscreen':
                    xbmc.executebuiltin('Action(togglefullscreen)')
                elif listItemAction == 'settings_audio':
                    func.open_window_id(var.WINDOW_DIALOG_AUDIO_OSD_SETTINGS)
                elif listItemAction == 'settings_video':
                    func.open_window_id(var.WINDOW_DIALOG_VIDEO_OSD_SETTINGS)
            elif clickId == 4000 and playerFull == True:
                self.hide_epg()

    def onAction(self, action):
        #Update the last interaction time
        self.InfoLastInteraction = datetime.now()

        #Check which action needs to execute
        actionId = action.getId()
        playerFull = self.getProperty('WebbiePlayerFull') == 'true'
        playerSeek = xbmc.getCondVisibility('Control.IsVisible(5000)')
        playerOpen = playerFull or playerSeek
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE) and playerOpen == False:
            close_the_page()
            return
        elif (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE) and playerOpen == True:
            self.hide_epg()
            return
        elif actionId == var.ACTION_MOVE_UP and playerFull == False:
            self.media_volume_up()
            return
        elif actionId == var.ACTION_MOVE_DOWN and playerFull == False:
            self.media_volume_down()
            return
        elif actionId == var.ACTION_MOVE_LEFT and playerFull == False:
            self.seek_back(True)
            return
        elif actionId == var.ACTION_MOVE_RIGHT and playerFull == False:
            self.seek_forward(True)
            return
        elif actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM:
            self.switch_channel_lasttv()
            return
        elif actionId == var.ACTION_NEXT_ITEM:
            self.switch_channel_nexttv()
            return
        elif actionId == var.ACTION_PREV_ITEM:
            self.switch_channel_previoustv()
            return
        elif self.block_input(actionId):
            return
        elif zap.check_remote_number(self, 1001, actionId, False, False):
            return
        elif playerFull == False:
            lastHideSeconds = int((datetime.now() - self.InfoLastHide).total_seconds())
            if lastHideSeconds >= 1:
                self.show_epg(False, False, True)
            return

    def block_input(self, actionId):
        if actionId == var.ACTION_NONE: return True
        elif actionId == var.ACTION_MUTE: return True
        elif actionId == var.ACTION_VOLUME_UP: return True
        elif actionId == var.ACTION_VOLUME_DOWN: return True
        elif actionId == var.ACTION_STEP_FORWARD: return True
        elif actionId == var.ACTION_STEP_BACK: return True
        elif actionId == var.ACTION_PLAYER_FORWARD: return True
        elif actionId == var.ACTION_PLAYER_REWIND: return True
        elif actionId == var.ACTION_PAUSE: return True
        elif actionId == var.ACTION_PLAYER_PLAY: return True
        elif actionId == var.ACTION_PLAYER_PLAYPAUSE: return True
        elif actionId == var.ACTION_MOUSE_RIGHT_CLICK: return True
        return False

    def start_threads(self):
        #Start update information thread
        var.thread_update_playergui_info.Start(self.thread_update_playergui_info)

        #Start hide information thread
        var.thread_hide_playergui_info.Start(self.thread_hide_playergui_info)

    def switch_subtitles(self):
        if xbmc.getCondVisibility("VideoPlayer.HasSubtitles"):
            xbmc.executebuiltin('Action(ShowSubtitles)')
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/subtitles.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ondertiteling niet beschikbaar.', notificationIcon, 2500, False)

    def thread_update_playergui_info(self):
        while var.thread_update_playergui_info.Allowed():
            try:
                var.thread_update_playergui_info.Sleep(400)
                playerSeek = xbmc.getCondVisibility('Control.IsVisible(5000)')
                if playerSeek:
                    self.update_epg_information()
            except:
                pass

    def thread_hide_playergui_info(self):
        while var.thread_hide_playergui_info.Allowed():
            try:
                lastInteractSeconds = int((datetime.now() - self.InfoLastInteraction).total_seconds())
                if lastInteractSeconds >= int(var.addon.getSetting('PlayerInformationCloseTime')):
                    self.hide_epg()
                else:
                    var.thread_hide_playergui_info.Sleep(1000)
            except:
                pass

    def thread_channel_delay_timer(self):
        while var.thread_channel_delay_timer.Allowed():
            try:
                xbmc.sleep(100)
                interactSecond = 3
                lastInteractSeconds = int((datetime.now() - self.ChannelDelay).total_seconds())

                #Channel information
                listContainer = self.getControl(1001)
                listItemSelected = listContainer.getSelectedItem()
                channelName = listItemSelected.getProperty("ChannelName")
                channelNumber = listItemSelected.getProperty("ChannelNumber")

                #Countdown string
                delayCountInt = interactSecond - lastInteractSeconds
                delayCountString = '[COLOR gray]' + str(delayCountInt) + '[/COLOR]'
                delayChannelString = func.get_provider_color_string() + channelNumber + '[/COLOR] ' + channelName

                #Show remaining time
                func.updateLabelText(self, 7001, delayCountString)
                func.updateLabelText(self, 7002, delayChannelString)
                self.setProperty('ZapVisible', 'true')

                #Change the channel
                if lastInteractSeconds >= interactSecond:
                    #Reset channel wait variables
                    var.thread_channel_delay_timer.Stop()
                    self.setProperty('ZapVisible', 'false')

                    #Switch to selected channel
                    streamplay.play_tv(listItemSelected, ShowInformation=True)
            except:
                pass

    def buttons_add_sidebar(self):
        #Get and check the list container
        listContainer = self.getControl(1002)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga naar vorige scherm')
        listItem.setProperty('ItemAction', 'media_previousscreen')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'),'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Afspelen of pauzeren')
        listItem.setProperty('ItemAction', 'media_playpause')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/playpause.png'),'icon': path.resources('resources/skins/default/media/common/playpause.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Stop met afspelen')
        listItem.setProperty('ItemAction', 'media_stop')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/stop.png'),'icon': path.resources('resources/skins/default/media/common/stop.png')})
        listContainer.addItem(listItem)

        if xbmc.getCondVisibility('System.Platform.Android') == False and xbmc.getCondVisibility('System.Platform.IOS') == False:
            listItem = xbmcgui.ListItem('Schakel tussen scherm modus')
            listItem.setProperty('ItemAction', 'media_fullscreen')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/fullscreen.png'),'icon': path.resources('resources/skins/default/media/common/fullscreen.png')})
            listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zap naar vorige zender')
        listItem.setProperty('ItemAction', 'media_lastchannel')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/last.png'),'icon': path.resources('resources/skins/default/media/common/last.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Volgend programma alarm')
        listItem.setProperty('ItemAction', 'media_alarmnext')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/alarm.png'),'icon': path.resources('resources/skins/default/media/common/alarm.png')})
        listContainer.addItem(listItem)

        if var.RecordingAccess() == True:
            listItem = xbmcgui.ListItem('Programma opnemen of annuleren')
            listItem.setProperty('ItemAction', 'media_record_event')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/record.png'),'icon': path.resources('resources/skins/default/media/common/record.png')})
            listContainer.addItem(listItem)

            listItem = xbmcgui.ListItem('Serie seizoen opnemen of annuleren')
            listItem.setProperty('ItemAction', 'media_record_series')
            listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/recordseries.png'),'icon': path.resources('resources/skins/default/media/common/recordseries.png')})
            listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Beheer de slaap timer')
        listItem.setProperty('ItemAction', 'media_sleep')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/sleep.png'),'icon': path.resources('resources/skins/default/media/common/sleep.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Stream achteruit spoelen')
        listItem.setProperty('ItemAction', 'media_seekback')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/seekback.png'),'icon': path.resources('resources/skins/default/media/common/seekback.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Stream vooruit spoelen')
        listItem.setProperty('ItemAction', 'media_seekforward')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/seekforward.png'),'icon': path.resources('resources/skins/default/media/common/seekforward.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Spoel naar live stream')
        listItem.setProperty('ItemAction', 'media_seeklive')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/seeklive.png'),'icon': path.resources('resources/skins/default/media/common/seeklive.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Spoel naar programma begin')
        listItem.setProperty('ItemAction', 'media_seekbegin')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/rerun.png'),'icon': path.resources('resources/skins/default/media/common/rerun.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Geluid volume omhoog')
        listItem.setProperty('ItemAction', 'media_volumeup')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumeup.png'),'icon': path.resources('resources/skins/default/media/common/volumeup.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Geluid volume omlaag')
        listItem.setProperty('ItemAction', 'media_volumedown')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumedown.png'),'icon': path.resources('resources/skins/default/media/common/volumedown.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Demp of ondemp geluid')
        listItem.setProperty('ItemAction', 'media_togglemute')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumemute.png'),'icon': path.resources('resources/skins/default/media/common/volumemute.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Ondertiteling aan of uit')
        listItem.setProperty('ItemAction', 'media_subtitlesonoff')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/subtitles.png'),'icon': path.resources('resources/skins/default/media/common/subtitles.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Geluids instellingen')
        listItem.setProperty('ItemAction', 'settings_audio')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/settingsaudio.png'),'icon': path.resources('resources/skins/default/media/common/settingsaudio.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Video instellingen')
        listItem.setProperty('ItemAction', 'settings_video')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/settingsvideo.png'),'icon': path.resources('resources/skins/default/media/common/settingsvideo.png')})
        listContainer.addItem(listItem)

        #Focus on the list
        self.setFocus(listContainer)
        xbmc.sleep(100)

        #Select list item
        listContainer.selectItem(0)
        xbmc.sleep(100)

    def set_alarm_next(self):
        #Get and check the list container
        listContainer = self.getControl(1001)
        selectedItem = listContainer.getSelectedItem()
        ProgramNextName = selectedItem.getProperty('ProgramNextNameRaw')
        ProgramNextTimeStartDateTime = func.datetime_from_string(selectedItem.getProperty("ProgramNextTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
        ChannelId = selectedItem.getProperty('ChannelId')
        ExternalId = selectedItem.getProperty('ExternalId')
        ChannelName = selectedItem.getProperty('ChannelName')

        #Check the program time
        if ProgramNextTimeStartDateTime != datetime(1970,1,1) and datetime.now() > ProgramNextTimeStartDateTime:
            notificationIcon = path.resources('resources/skins/default/media/common/alarm.png')
            xbmcgui.Dialog().notification(var.addonname, 'Programma is al afgelopen.', notificationIcon, 2500, False)
            return

        #Set or remove the next program alarm
        alarmAdded = alarm.alarm_add(ProgramNextTimeStartDateTime, ChannelId, ExternalId, ChannelName, ProgramNextName, True)

        #Update alarm icon in the information
        if alarmAdded == True:
            selectedItem.setProperty("ProgramNextAlarm", 'true')
        elif alarmAdded == 'Remove':
            selectedItem.setProperty("ProgramNextAlarm", 'false')

    def media_volume_up(self):
        #Check if volume is muted
        volumeMuted = xbmc.getCondVisibility('Player.Muted')
        if volumeMuted:
            xbmc.executebuiltin('Action(Mute)')

        #Change the volume up
        xbmc.executebuiltin('Action(VolumeUp)')

    def media_volume_down(self):
        #Check if volume is muted
        volumeMuted = xbmc.getCondVisibility('Player.Muted')
        if volumeMuted:
            xbmc.executebuiltin('Action(Mute)')

        #Change the volume down
        xbmc.executebuiltin('Action(VolumeDown)')

    def seek_forward(self, showEpg=False):
        xbmc.executebuiltin('Action(StepForward)')

        #Show the epg and select channel
        if showEpg:
            self.show_epg(True, True, True)
            return

        #Select channel in list container
        CurrentChannelId = var.addon.getSetting('CurrentChannelId')
        lifunc.focus_on_channelid_in_list(self, 1001, 0, False, CurrentChannelId)

    def seek_back(self, showEpg=False):
        xbmc.executebuiltin('Action(StepBack)')

        #Show the epg and select channel
        if showEpg:
            self.show_epg(True, True, True)
            return

        #Select channel in list container
        CurrentChannelId = var.addon.getSetting('CurrentChannelId')
        lifunc.focus_on_channelid_in_list(self, 1001, 0, False, CurrentChannelId)

    def seek_begin_program(self):
        #Get and check the list container
        listContainer = self.getControl(1001)
        selectedItem = listContainer.getSelectedItem()
        ProgramNowTimeStartDateTime = func.datetime_from_string(selectedItem.getProperty("ProgramNowTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')

        #Check the program start time
        if ProgramNowTimeStartDateTime != datetime(1970,1,1):
            playingSeconds = int((datetime.now() - ProgramNowTimeStartDateTime).total_seconds())
            totalSeconds = int(xbmc.Player().getTotalTime())
            seekSeconds = totalSeconds - playingSeconds + 10
            if seekSeconds >= 0:
                #Seek to program beginning
                xbmc.Player().seekTime(seekSeconds)
                notificationIcon = path.resources('resources/skins/default/media/common/rerun.png')
                xbmcgui.Dialog().notification(var.addonname, 'Naar programma begin gespoeld.', notificationIcon, 2500, False)

                #Select channel in list container
                CurrentChannelId = var.addon.getSetting('CurrentChannelId')
                lifunc.focus_on_channelid_in_list(self, 1001, 0, False, CurrentChannelId)
            else:
                notificationIcon = path.resources('resources/skins/default/media/common/rerun.png')
                xbmcgui.Dialog().notification(var.addonname, 'Programma begin niet beschikbaar.', notificationIcon, 2500, False)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/rerun.png')
            xbmcgui.Dialog().notification(var.addonname, 'Start tijd is onbekend.', notificationIcon, 2500, False)

    def seek_live(self):
        #Seek to live position
        seekSeconds = int(xbmc.Player().getTotalTime())
        xbmc.Player().seekTime(seekSeconds)
        notificationIcon = path.resources('resources/skins/default/media/common/seeklive.png')
        xbmcgui.Dialog().notification(var.addonname, 'De stream is nu live.', notificationIcon, 2500, False)

        #Select channel in list container
        CurrentChannelId = var.addon.getSetting('CurrentChannelId')
        lifunc.focus_on_channelid_in_list(self, 1001, 0, False, CurrentChannelId)

    def switch_channel_lasttv(self):
        if var.TelevisionChannelListItemLast != None:
            notificationIcon = path.resources('resources/skins/default/media/common/last.png')
            xbmcgui.Dialog().notification(var.addonname, 'Gezapt naar vorige zender.', notificationIcon, 2500, False)
            streamplay.play_tv(var.TelevisionChannelListItemLast, ShowInformation=True)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/last.png')
            xbmcgui.Dialog().notification(var.addonname, 'Geen vorige zender beschikbaar.', notificationIcon, 2500, False)

    def switch_channel_nexttv(self):
        self.ChannelDelay = datetime.now()
        listContainer = self.getControl(1001)
        self.setFocus(listContainer)
        xbmc.sleep(100)
        listContainer.selectItem(listContainer.getSelectedPosition() + 1)
        xbmc.sleep(100)
        self.show_epg(False, False, False)
        #Start the channel wait thread
        var.thread_channel_delay_timer.Start(self.thread_channel_delay_timer)

    def switch_channel_previoustv(self):
        self.ChannelDelay = datetime.now()
        listContainer = self.getControl(1001)
        self.setFocus(listContainer)
        xbmc.sleep(100)
        listContainer.selectItem(listContainer.getSelectedPosition() - 1)
        xbmc.sleep(100)
        self.show_epg(False, False, False)
        #Start the channel wait thread
        var.thread_channel_delay_timer.Start(self.thread_channel_delay_timer)

    def load_channels(self, forceLoad=False):
        self.EpgPauseUpdate = True
        xbmc.sleep(250) #Wait for epg update to pause
        self.load_channels_code(forceLoad)
        self.EpgPauseUpdate = False

    def load_channels_code(self, forceLoad=False):
        #Get and check the list container
        listContainer = self.getControl(1001)
        if forceLoad == False:
            if listContainer.size() > 0:
                return True
        else:
            listContainer.reset()

        #Add items to list container
        if lichanneltelevision.list_load_combined(listContainer) == False:
            return False

        #Select channel in list container
        currentChannelId = var.addon.getSetting('CurrentChannelId')
        lifunc.focus_on_channelid_in_list(self, 1001, 0, False, currentChannelId)

    def hide_epg(self):
        #Update the last hide time
        self.InfoLastHide = datetime.now()

        #Hide the epg interface
        self.setProperty('WebbiePlayerFull', 'false')
        self.setProperty('WebbiePlayerSeek', 'false')

    def show_epg(self, seekInterface=False, removeFocus=False, selectCurrentChannel=True):
        #Update the last interaction time
        self.InfoLastInteraction = datetime.now()

        #Show the epg interface
        if seekInterface == False:
            self.setProperty('WebbiePlayerFull', 'true')
        else:
            self.setProperty('WebbiePlayerSeek', 'true')

        #Select the current channel
        if selectCurrentChannel:
            currentChannelId = var.addon.getSetting('CurrentChannelId')
            lifunc.focus_on_channelid_in_list(self, 1001, 0, True, currentChannelId)

        #Remove focus from the interface
        if removeFocus:
            listControl = self.getControl(4000)
            self.setFocus(listControl)
            xbmc.sleep(100)

    def update_epg_information(self):
        try:
            #Check if epg is allowed to update
            if self.EpgPauseUpdate: return

            #Get and check the list container
            listContainer = self.getControl(1001)

            #Generate and update program summary
            updateItem = listContainer.getSelectedItem()
            liplayergui.list_update(updateItem)
        except:
            pass
