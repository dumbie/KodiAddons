import json
from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import alarm
import channellist
import download
import favorite
import func
import path
import programsummary
import recordingfunc
import sleep
import stream
import var
import zap

def switch_to_page():
    if var.guiPlayer == None:
        var.guiPlayer = Gui('playergui.xml', var.addonpath, 'default', '720p')
        var.guiPlayer.show()

def close_the_page():
    if var.guiPlayer != None:
        #Stop the update information thread
        var.thread_update_playergui_info = None

        #Stop the hide information thread
        var.thread_hide_playergui_info = None

        #Close the custom video player window
        var.guiPlayer.close()
        var.guiPlayer = None

        #Close the fullscreen media player
        func.close_window_id(var.WINDOW_FULLSCREEN_VIDEO)

class Gui(xbmcgui.WindowXMLDialog):
    PlayerInfoLastInteraction = datetime(1970, 1, 1)
    PlayerInfoLastHide = datetime(1970, 1, 1)

    def onInit(self):
        self.buttons_add_sidebar()
        favorite.favorite_json_load()
        self.load_channels()
        self.load_recording_event(False)
        self.load_recording_series(False)

        #Wait for previous threads to complete
        if var.thread_update_playergui_info != None:
            var.thread_update_playergui_info = None
            xbmc.sleep(500)
        if var.thread_hide_playergui_info != None:
            var.thread_hide_playergui_info = None
            xbmc.sleep(500)

        #Start the update information thread
        if var.thread_update_playergui_info == None:
            var.thread_update_playergui_info = Thread(target=self.thread_update_playergui_info)
            var.thread_update_playergui_info.start()

        #Start the hide information thread
        if var.thread_hide_playergui_info == None:
            var.thread_hide_playergui_info = Thread(target=self.thread_hide_playergui_info)
            var.thread_hide_playergui_info.start()

    def onClick(self, clickId):
        if var.thread_zap_wait_timer == None:
            clickedControl = self.getControl(clickId)
            playerFull = self.getProperty('WebbiePlayerFull') == 'true'
            if clickId == 1001 and playerFull == True:
                listItemSelectedClicked = clickedControl.getSelectedItem()
                stream.switch_channel_tv_listitem(listItemSelectedClicked, False, True)
            elif clickId == 1002 and playerFull == True:
                listItemSelectedClicked = clickedControl.getSelectedItem()
                listItemAction = listItemSelectedClicked.getProperty('Action')
                if listItemAction == 'media_lastchannel':
                    self.switch_channel_lasttv()
                elif listItemAction == 'media_sleep':
                    sleep.dialog_sleep()
                elif listItemAction == 'media_alarmnext':
                    self.set_alarm_next()
                elif listItemAction == 'media_record_event':
                    listcontainer = self.getControl(1001)
                    listItemSelectedChannel = listcontainer.getSelectedItem()
                    recordingfunc.record_event_now_television_playergui(listItemSelectedChannel)
                elif listItemAction == 'media_record_series':
                    listcontainer = self.getControl(1001)
                    listItemSelectedChannel = listcontainer.getSelectedItem()
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
                    xbmc.Player().stop()
                elif listItemAction == 'media_playpause':
                    xbmc.Player().pause()
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
        self.PlayerInfoLastInteraction = datetime.now()

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
            lastHideSeconds = int((datetime.now() - self.PlayerInfoLastHide).total_seconds())
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

    def switch_subtitles(self):
        if xbmc.getCondVisibility("VideoPlayer.HasSubtitles"):
            xbmc.executebuiltin('Action(ShowSubtitles)')
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/subtitles.png')
            xbmcgui.Dialog().notification(var.addonname, 'Ondertiteling niet beschikbaar.', notificationIcon, 2500, False)

    def thread_update_playergui_info(self):
        while var.thread_update_playergui_info != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
            playerSeek = xbmc.getCondVisibility('Control.IsVisible(5000)')
            if playerSeek:
                self.update_epg_information()
            xbmc.sleep(200)

    def thread_hide_playergui_info(self):
        while var.thread_hide_playergui_info != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
            lastInteractSeconds = int((datetime.now() - self.PlayerInfoLastInteraction).total_seconds())
            if lastInteractSeconds >= int(var.addon.getSetting('PlayerInformationCloseTime')):
                self.hide_epg()
            else:
                xbmc.sleep(1000)

    def thread_channel_delay_timer(self):
        while var.thread_channel_delay_timer != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
            xbmc.sleep(100)
            interactSecond = 3
            lastInteractSeconds = int((datetime.now() - var.ChannelDelayDateTime).total_seconds())

            #Channel information
            listcontainer = self.getControl(1001)
            listItemSelected = listcontainer.getSelectedItem()
            channelNameProp = listItemSelected.getProperty("ChannelName")
            channelNumberProp = listItemSelected.getProperty("ChannelNumber")

            #Countdown string
            delayCountInt = interactSecond - lastInteractSeconds
            delayCountString = '[COLOR gray]' + str(delayCountInt) + '[/COLOR] ' + func.get_provider_color_string() + channelNumberProp + '[/COLOR] [COLOR white]' + channelNameProp + '[/COLOR]'

            #Show remaining time
            func.updateLabelText(self, 7001, delayCountString)
            self.setProperty('ZapVisible', 'true')

            #Change the channel
            if lastInteractSeconds >= interactSecond:
                #Reset channel wait variables
                var.thread_channel_delay_timer = None
                self.setProperty('ZapVisible', 'false')

                #Switch to selected channel
                stream.switch_channel_tv_listitem(listItemSelected, False, False)

    def buttons_add_sidebar(self):
        #Get and check the list container
        listcontainer = self.getControl(1002)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga naar vorige scherm')
        listitem.setProperty('Action', 'media_previousscreen')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'),'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Afspelen of pauzeren')
        listitem.setProperty('Action', 'media_playpause')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/playpause.png'),'icon': path.resources('resources/skins/default/media/common/playpause.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Stop met afspelen')
        listitem.setProperty('Action', 'media_stop')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/stop.png'),'icon': path.resources('resources/skins/default/media/common/stop.png')})
        listcontainer.addItem(listitem)

        if xbmc.getCondVisibility('System.Platform.Android') == False and xbmc.getCondVisibility('System.Platform.IOS') == False:
            listitem = xbmcgui.ListItem('Schakel tussen scherm modus')
            listitem.setProperty('Action', 'media_fullscreen')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/fullscreen.png'),'icon': path.resources('resources/skins/default/media/common/fullscreen.png')})
            listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zap naar vorige zender')
        listitem.setProperty('Action', 'media_lastchannel')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/last.png'),'icon': path.resources('resources/skins/default/media/common/last.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Volgend programma alarm')
        listitem.setProperty('Action', 'media_alarmnext')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/alarm.png'),'icon': path.resources('resources/skins/default/media/common/alarm.png')})
        listcontainer.addItem(listitem)

        if var.RecordingAccess == True:
            listitem = xbmcgui.ListItem('Programma opnemen of annuleren')
            listitem.setProperty('Action', 'media_record_event')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/record.png'),'icon': path.resources('resources/skins/default/media/common/record.png')})
            listcontainer.addItem(listitem)

            listitem = xbmcgui.ListItem('Serie seizoen opnemen of annuleren')
            listitem.setProperty('Action', 'media_record_series')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/recordseries.png'),'icon': path.resources('resources/skins/default/media/common/recordseries.png')})
            listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Beheer de slaap timer')
        listitem.setProperty('Action', 'media_sleep')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/sleep.png'),'icon': path.resources('resources/skins/default/media/common/sleep.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Stream achteruit spoelen')
        listitem.setProperty('Action', 'media_seekback')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/seekback.png'),'icon': path.resources('resources/skins/default/media/common/seekback.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Stream vooruit spoelen')
        listitem.setProperty('Action', 'media_seekforward')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/seekforward.png'),'icon': path.resources('resources/skins/default/media/common/seekforward.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Spoel naar live stream')
        listitem.setProperty('Action', 'media_seeklive')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/seeklive.png'),'icon': path.resources('resources/skins/default/media/common/seeklive.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Spoel naar programma begin')
        listitem.setProperty('Action', 'media_seekbegin')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/rerun.png'),'icon': path.resources('resources/skins/default/media/common/rerun.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Geluid volume omhoog')
        listitem.setProperty('Action', 'media_volumeup')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumeup.png'),'icon': path.resources('resources/skins/default/media/common/volumeup.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Geluid volume omlaag')
        listitem.setProperty('Action', 'media_volumedown')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumedown.png'),'icon': path.resources('resources/skins/default/media/common/volumedown.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Demp of ondemp geluid')
        listitem.setProperty('Action', 'media_togglemute')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumemute.png'),'icon': path.resources('resources/skins/default/media/common/volumemute.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Ondertiteling aan of uit')
        listitem.setProperty('Action', 'media_subtitlesonoff')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/subtitles.png'),'icon': path.resources('resources/skins/default/media/common/subtitles.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Geluids instellingen')
        listitem.setProperty('Action', 'settings_audio')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/settingsaudio.png'),'icon': path.resources('resources/skins/default/media/common/settingsaudio.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Video instellingen')
        listitem.setProperty('Action', 'settings_video')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/settingsvideo.png'),'icon': path.resources('resources/skins/default/media/common/settingsvideo.png')})
        listcontainer.addItem(listitem)

        #Focus on the list
        self.setFocus(listcontainer)
        xbmc.sleep(100)

        #Select list item
        listcontainer.selectItem(0)
        xbmc.sleep(100)

    def set_alarm_next(self):
        #Get and check the list container
        listcontainer = self.getControl(1001)
        selectedItem = listcontainer.getSelectedItem()
        ProgramNextName = selectedItem.getProperty('ProgramNextName')
        ProgramNextTimeStartDateTime = func.datetime_from_string(selectedItem.getProperty("ProgramNextTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
        ChannelId = selectedItem.getProperty('ChannelId')
        ExternalId = selectedItem.getProperty('ExternalId')
        ChannelName = selectedItem.getProperty('ChannelName')

        #Check the program time
        if ProgramNextTimeStartDateTime != datetime(1970, 1, 1) and datetime.now() > ProgramNextTimeStartDateTime:
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

    def media_pause(self):
        #Check if stream is paused
        playerPaused = xbmc.getCondVisibility("Player.Paused")
        if playerPaused == False:
            xbmc.Player().pause()

    def media_volume_up(self):
        #Check if volume is muted
        volumeMuted = xbmc.getCondVisibility('Player.Muted')
        if volumeMuted:
            xbmc.executebuiltin('Action(Mute)')

        #Change the volume up
        JSONRPC = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["volume"]}, "id": 1}')
        volumeCurrent = json.loads(JSONRPC)["result"]["volume"]
        volumeStep = int(var.addon.getSetting('PlayerVolumeStep')) * -1
        volumeTarget = str(volumeCurrent - volumeStep)
        xbmc.executebuiltin('SetVolume(' + volumeTarget + ',showVolumeBar)')

    def media_volume_down(self):
        #Check if volume is muted
        volumeMuted = xbmc.getCondVisibility('Player.Muted')
        if volumeMuted:
            xbmc.executebuiltin('Action(Mute)')

        #Change the volume down
        JSONRPC = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["volume"]}, "id": 1}')
        volumeCurrent = json.loads(JSONRPC)["result"]["volume"]
        volumeStep = int(var.addon.getSetting('PlayerVolumeStep')) * -1
        volumeTarget = str(volumeCurrent + volumeStep)
        xbmc.executebuiltin('SetVolume(' + volumeTarget + ',showVolumeBar)')

    def seek_forward(self, showEpg=False):
        xbmc.executebuiltin('Action(StepForward)')

        #Show the epg and select channel
        if showEpg:
            self.show_epg(True, True, True)
            return

        #Select channel in list container
        CurrentChannelId = var.addon.getSetting('CurrentChannelId')
        func.focus_on_channel_list(self, 1001, 0, False, CurrentChannelId)

    def seek_back(self, showEpg=False):
        xbmc.executebuiltin('Action(StepBack)')

        #Show the epg and select channel
        if showEpg:
            self.show_epg(True, True, True)
            return

        #Select channel in list container
        CurrentChannelId = var.addon.getSetting('CurrentChannelId')
        func.focus_on_channel_list(self, 1001, 0, False, CurrentChannelId)

    def seek_begin_program(self):
        #Get and check the list container
        listcontainer = self.getControl(1001)
        selectedItem = listcontainer.getSelectedItem()

        ProgramNowTimeStartDateTime = func.datetime_from_string(selectedItem.getProperty("ProgramNowTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')

        #Check the program start time
        if ProgramNowTimeStartDateTime != datetime(1970, 1, 1):
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
                func.focus_on_channel_list(self, 1001, 0, False, CurrentChannelId)
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
        func.focus_on_channel_list(self, 1001, 0, False, CurrentChannelId)

    def switch_channel_lasttv(self):
        LastAssetId = var.addon.getSetting('LastAssetId')
        LastChannelId = var.addon.getSetting('LastChannelId')
        LastExternalId = var.addon.getSetting('LastExternalId')
        LastChannelName = var.addon.getSetting('LastChannelName')
        CurrentChannelId = var.addon.getSetting('CurrentChannelId')
        if LastChannelId != CurrentChannelId:
            notificationIcon = path.resources('resources/skins/default/media/common/last.png')
            xbmcgui.Dialog().notification(var.addonname, 'Gezapt naar vorige zender.', notificationIcon, 2500, False)
            stream.switch_channel_tv_channelid(LastAssetId, LastChannelId, LastExternalId, LastChannelName, 'Televisie', False, True)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/last.png')
            xbmcgui.Dialog().notification(var.addonname, 'Geen vorige zender beschikbaar.', notificationIcon, 2500, False)

    def switch_channel_nexttv(self):
        var.ChannelDelayDateTime = datetime.now()
        self.media_pause()
        listcontainer = self.getControl(1001)
        self.setFocus(listcontainer)
        xbmc.sleep(100)
        listcontainer.selectItem(listcontainer.getSelectedPosition() + 1)
        xbmc.sleep(100)
        self.show_epg(False, False, False)
        #Start the channel wait thread
        if var.thread_channel_delay_timer == None:
            var.thread_channel_delay_timer = Thread(target=self.thread_channel_delay_timer)
            var.thread_channel_delay_timer.start()

    def switch_channel_previoustv(self):
        var.ChannelDelayDateTime = datetime.now()
        self.media_pause()
        listcontainer = self.getControl(1001)
        self.setFocus(listcontainer)
        xbmc.sleep(100)
        listcontainer.selectItem(listcontainer.getSelectedPosition() - 1)
        xbmc.sleep(100)
        self.show_epg(False, False, False)
        #Start the channel wait thread
        if var.thread_channel_delay_timer == None:
            var.thread_channel_delay_timer = Thread(target=self.thread_channel_delay_timer)
            var.thread_channel_delay_timer.start()

    def load_recording_event(self, forceUpdate=False):
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False: return False

    def load_recording_series(self, forceUpdate=False):
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False: return False

    def load_channels(self):
        #Get and check the list container
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        #Download the channels
        downloadResult = download.download_channels_tv(False)
        if downloadResult == False: return False

        #Add channels to list
        channellist.channel_list_load(listcontainer)

        #Select channel in list container
        currentChannelId = var.addon.getSetting('CurrentChannelId')
        func.focus_on_channel_list(self, 1001, 0, False, currentChannelId)

    def hide_epg(self):
        #Update the last hide time
        self.PlayerInfoLastHide = datetime.now()

        #Hide the epg interface
        self.setProperty('WebbiePlayerFull', 'false')
        self.setProperty('WebbiePlayerSeek', 'false')

    def show_epg(self, seekInterface=False, removeFocus=False, selectChannel=True):
        #Show the epg interface
        if seekInterface == False:
            self.setProperty('WebbiePlayerFull', 'true')
        else:
            self.setProperty('WebbiePlayerSeek', 'true')

        #Select the current channel
        if selectChannel:
            currentChannelId = var.addon.getSetting('CurrentChannelId')
            func.focus_on_channel_list(self, 1001, 0, True, currentChannelId)

        #Remove focus from the interface
        if removeFocus:
            listControl = self.getControl(4000)
            self.setFocus(listControl)
            xbmc.sleep(100)

    def update_epg_information(self):
        #Download epg information today
        download.download_epg_day(datetime.now().strftime('%Y-%m-%d'))

        #Get and check the list container
        listcontainer = self.getControl(1001)

        #Generate program summary for playergui
        try:
            updateItem = listcontainer.getSelectedItem()
            programsummary.program_summary_playergui(updateItem)
        except:
            pass
