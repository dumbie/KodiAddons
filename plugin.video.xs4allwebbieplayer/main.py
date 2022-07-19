from threading import Thread
import kids
import xbmc
import xbmcgui
import alarm
import apilogin
import default
import dialog
import epg
import func
import helpx
import movies
import path
import radio
import recorded
import recordingevent
import recordingseries
import search
import series
import sleep
import sport
import stream
import television
import var
import widevine
import yesterday

def switch_to_page():
    if var.guiMain == None:
        var.guiMain = Gui('main.xml', var.addonpath, 'default', '720p')
        var.guiMain.doModal()
        var.guiMain = None

def close_the_page():
    if var.guiMain != None:
        #Stop the playing media
        xbmc.Player().stop()

        #Stop the addon threads
        default.stop_addon_threads()

        #Clear used global variables
        default.clear_home_variables()

        #Close the shown window
        var.guiMain.close()

def dialog_close():
    dialogAnswers = ['Webbie Player afsluiten', 'Apparaat uitschakelen', 'Apparaat herstarten', 'Kodi afsluiten']
    if xbmc.Player().isPlayingVideo():
        dialogAnswers.insert(0, 'Toon video speler')

    dialogHeader = 'Sluiten'

    if xbmc.Player().isPlaying():
        dialogSummary = 'Wat wilt u doen? als u afsluit zal de spelende media ook stoppen.'
    else:
        dialogSummary = 'Wat wilt u doen?'

    dialogFooter = ''

    dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
    if dialogResult == 'Webbie Player afsluiten':
        close_the_page()
    elif dialogResult == 'Apparaat uitschakelen':
        func.device_shutdown_dialog()
    elif dialogResult == 'Apparaat herstarten':
        func.device_reboot_dialog()
    elif dialogResult == 'Kodi afsluiten':
        func.close_kodi_dialog()
    elif dialogResult == 'Toon video speler':
        var.PlayerCustom.Fullscreen(True)
    else:
        var.guiMain.check_focus()

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Check if logged in on launch
        if var.ApiLoggedIn == False:
            func.updateLabelText(self, 1, "Aan het aanmelden.")
            apilogin.ApiLogin(False)

        #Update the current login status
        if var.ApiLoggedIn == True:
            func.updateLabelText(self, 1, "Aangemeld, veel kijkplezier.")
        else:
            func.updateLabelText(self, 1, "Aanmelden is mislukt.")

        #Add menu buttons to the page
        menuButtons = self.buttons_add_menu()

        #Add media buttons to the page
        self.buttons_add_media(False)

        #Focus on the menu buttons
        listcontainer = self.getControl(1000)
        self.setFocus(listcontainer)
        xbmc.sleep(100)

        #Update the active alarms count
        self.count_alarm(True)

        #Update the recorded event count
        self.count_recorded_event()

        #Update the recording event count
        self.count_recording_event()

        #Update the recording series count
        self.count_recording_series()

        #Check if menu is already filled / prevent one time code
        if menuButtons == True:
            return

        #Check if Widevine is installed
        if var.thread_check_requirements == None:
            var.thread_check_requirements = Thread(target=widevine.thread_check_requirements)
            var.thread_check_requirements.start()

        #Check television favorite setting
        if var.addon.getSetting('TelevisionChannelFavorite') == 'true':
            var.LoadChannelFavoritesOnly = True
        else:
            var.LoadChannelFavoritesOnly = False

        #Check if user is logged in
        if var.ApiLoggedIn == True:
            #Open the last known television channel
            if var.addon.getSetting('StartWithLastChannel') == 'true' and var.addon.getSetting('StartWithKids') == 'false':
                CurrentAssetId = var.addon.getSetting('CurrentAssetId')
                CurrentChannelId = var.addon.getSetting('CurrentChannelId')
                CurrentExternalId = var.addon.getSetting('CurrentExternalId')
                CurrentChannelName = var.addon.getSetting('CurrentChannelName')
                stream.switch_channel_tv_channelid(CurrentAssetId, CurrentChannelId, CurrentExternalId, CurrentChannelName, 'Televisie', True, False)

            #Go to the desired page on startup
            if var.addon.getSetting('StartWithTelevision') == 'true':
                television.switch_to_page()
            elif var.addon.getSetting('StartWithKids') == 'true':
                kids.switch_to_page()

    def buttons_add_media(self, resetButtons):
        #Get and check the media control list container
        listcontainer = self.getControl(1001)
        if resetButtons:
            listcontainer.reset()
            listcontainer = self.getControl(1000)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            return

        if xbmc.Player().isPlaying():
            #Add stop button
            if listcontainer.size() == 0:
                listitem = xbmcgui.ListItem('Stop met afspelen')
                listitem.setProperty('Action', 'media_stop')
                listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/stop.png'),'icon': path.resources('resources/skins/default/media/common/stop.png')})
                listcontainer.addItem(listitem)

            #Add mute button
            if listcontainer.size() == 1:
                listitem = xbmcgui.ListItem('On/demp het geluid')
                listitem.setProperty('Action', 'media_togglemute')
                listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumemute.png'),'icon': path.resources('resources/skins/default/media/common/volumemute.png')})
                listcontainer.addItem(listitem)

            #Add fullscreen button
            if xbmc.Player().isPlayingVideo():
                if listcontainer.size() == 2:
                    listitem = xbmcgui.ListItem()
                    listitem.setLabel('Toon video speler')
                    listitem.setProperty('Action', 'media_fullscreen')
                    listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/fullscreen.png'),'icon': path.resources('resources/skins/default/media/common/fullscreen.png')})
                    listcontainer.addItem(listitem)
                elif listcontainer.size() == 3:
                    updateItem = listcontainer.getListItem(2)
                    updateItem.setLabel('Toon video speler')
                    updateItem.setProperty('Action', 'media_fullscreen')
                    updateItem.setArt({'thumb': path.resources('resources/skins/default/media/common/fullscreen.png'),'icon': path.resources('resources/skins/default/media/common/fullscreen.png')})
            elif xbmc.Player().isPlayingAudio():
                if listcontainer.size() == 2:
                    listitem = xbmcgui.ListItem()
                    listitem.setLabel('Toon visualisatie')
                    listitem.setProperty('Action', 'show_visualisation')
                    listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/visualisation.png'),'icon': path.resources('resources/skins/default/media/common/visualisation.png')})
                    listcontainer.addItem(listitem)
                elif listcontainer.size() == 3:
                    updateItem = listcontainer.getListItem(2)
                    updateItem.setLabel('Toon visualisatie')
                    updateItem.setProperty('Action', 'show_visualisation')
                    updateItem.setArt({'thumb': path.resources('resources/skins/default/media/common/visualisation.png'),'icon': path.resources('resources/skins/default/media/common/visualisation.png')})
            elif listcontainer.size() == 3:
                listcontainer.removeItem(2)
                xbmc.sleep(100)
        else:
            listcontainer.reset()
            listcontainer = self.getControl(1000)
            self.setFocus(listcontainer)
            xbmc.sleep(100)

    def buttons_add_menu(self):
        #Get and check the main list container
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0: return True

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('Televisie')
            listitem.setProperty('Action', 'page_television')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/television.png'),'icon': path.resources('resources/skins/default/media/common/television.png')})
            listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Radio')
        listitem.setProperty('Action', 'page_radio')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/radio.png'), 'icon': path.resources('resources/skins/default/media/common/radio.png')})
        listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('Films')
            listitem.setProperty('Action', 'page_movies')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/movies.png'), 'icon': path.resources('resources/skins/default/media/common/movies.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('Series')
            listitem.setProperty('Action', 'page_series')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/series.png'), 'icon': path.resources('resources/skins/default/media/common/series.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('TV Gids')
            listitem.setProperty('Action', 'page_epg')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/epg.png'), 'icon': path.resources('resources/skins/default/media/common/epg.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('Zoeken')
            listitem.setProperty('Action', 'page_search')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('Sport Gemist')
            listitem.setProperty('Action', 'page_sport')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/sport.png'), 'icon': path.resources('resources/skins/default/media/common/sport.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('Gister Gemist')
            listitem.setProperty('Action', 'page_yesterday')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/vod.png'), 'icon': path.resources('resources/skins/default/media/common/vod.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            if var.addon.getSetting('KidsPageLock') == 'true':
                listitem = xbmcgui.ListItem('Kids met slot')
            else:
                listitem = xbmcgui.ListItem('Kids')
            listitem.setProperty('Action', 'page_kids')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/kids.png'), 'icon': path.resources('resources/skins/default/media/common/kids.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True and var.RecordingAccess == True:
            listitem = xbmcgui.ListItem('Bekijk Opnames (?)')
            listitem.setProperty('Action', 'page_recorded')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/recorddone.png'), 'icon': path.resources('resources/skins/default/media/common/recorddone.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True and var.RecordingAccess == True:
            listitem = xbmcgui.ListItem('Geplande Opnames (?)')
            listitem.setProperty('Action', 'page_recording_event')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/record.png'), 'icon': path.resources('resources/skins/default/media/common/record.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True and var.RecordingAccess == True:
            listitem = xbmcgui.ListItem('Geplande Series (?)')
            listitem.setProperty('Action', 'page_recording_series')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/recordseries.png'), 'icon': path.resources('resources/skins/default/media/common/recordseries.png')})
            listcontainer.addItem(listitem)

        if var.ApiLoggedIn == True:
            listitem = xbmcgui.ListItem('Alarmen (?)')
            listitem.setProperty('Action', 'page_alarm')
            listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/alarm.png'), 'icon': path.resources('resources/skins/default/media/common/alarm.png')})
            listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Slaap Timer')
        listitem.setProperty('Action', 'page_sleep')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/sleep.png'), 'icon': path.resources('resources/skins/default/media/common/sleep.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Instellingen')
        listitem.setProperty('Action', 'addon_settings')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/settings.png'), 'icon': path.resources('resources/skins/default/media/common/settings.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Help')
        listitem.setProperty('Action', 'page_help')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/help.png'), 'icon': path.resources('resources/skins/default/media/common/help.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Sluiten')
        listitem.setProperty('Action', 'addon_shutdown')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/shutdown.png'), 'icon': path.resources('resources/skins/default/media/common/shutdown.png')})
        listcontainer.addItem(listitem)

    def count_recorded_event(self):
        try:
            #Get and check the main list container
            listcontainer = self.getControl(1000)
            if listcontainer.size() == 0 or var.ApiLoggedIn == False:
                return False

            #Load and count the planned recording
            recordingCount = recorded.count_main_recording()

            #Update the list count
            countItem = func.search_label_listcontainer(listcontainer, 'Bekijk Opnames')
            countItem.setLabel('Bekijk Opnames (' + str(recordingCount) + ')')
        except:
            pass

    def count_recording_event(self):
        try:
            #Get and check the main list container
            listcontainer = self.getControl(1000)
            if listcontainer.size() == 0 or var.ApiLoggedIn == False:
                return False

            #Load and count the planned recording
            recordingCount = recordingevent.count_main_recording()

            #Update the list count
            countItem = func.search_label_listcontainer(listcontainer, 'Geplande Opnames')
            countItem.setLabel('Geplande Opnames (' + str(recordingCount) + ')')
        except:
            pass

    def count_recording_series(self):
        try:
            #Get and check the main list container
            listcontainer = self.getControl(1000)
            if listcontainer.size() == 0 or var.ApiLoggedIn == False:
                return False

            #Load and count the planned recording
            recordingCount = recordingseries.count_main_recording()

            #Update the list count
            countItem = func.search_label_listcontainer(listcontainer, 'Geplande Series')
            countItem.setLabel('Geplande Series (' + str(recordingCount) + ')')
        except:
            pass

    def count_alarm(self, forceLoad=False):
        try:
            #Get and check the main list container
            listcontainer = self.getControl(1000)
            if listcontainer.size() == 0 or var.ApiLoggedIn == False:
                return False

            #Load the program alarms
            alarm.alarm_json_load(forceLoad)

            #Update the list count
            countItem = func.search_label_listcontainer(listcontainer, 'Alarmen')
            countItem.setLabel('Alarmen (' + str(len(var.AlarmDataJson)) + ')')
        except:
            pass

    def check_focus(self):
        focusNavigation = xbmc.getCondVisibility('Control.HasFocus(1001)')
        focusMain = xbmc.getCondVisibility('Control.HasFocus(1000)')
        if focusNavigation:
            focusControl = self.getControl(1001)
            self.setFocus(focusControl)
            xbmc.sleep(100)
        elif focusMain:
            focusControl = self.getControl(1000)
            self.setFocus(focusControl)
            xbmc.sleep(100)

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            dialog_close()

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'page_television':
                television.switch_to_page()
            elif listItemAction == 'page_radio':
                radio.switch_to_page()
            elif listItemAction == 'page_yesterday':
                yesterday.switch_to_page()
            elif listItemAction == 'page_kids':
                kids.switch_to_page()
            elif listItemAction == 'page_recorded':
                recorded.switch_to_page()
            elif listItemAction == 'page_search':
                search.switch_to_page()
            elif listItemAction == 'page_movies':
                movies.switch_to_page()
            elif listItemAction == 'page_series':
                series.switch_to_page()
            elif listItemAction == 'page_sport':
                sport.switch_to_page()
            elif listItemAction == 'page_epg':
                epg.switch_to_page()
            elif listItemAction == 'page_sleep':
                sleep.dialog_sleep()
            elif listItemAction == 'page_alarm':
                alarm.switch_to_page()
            elif listItemAction == 'page_recording_event':
                recordingevent.switch_to_page()
            elif listItemAction == 'page_recording_series':
                recordingseries.switch_to_page()
            elif listItemAction == 'addon_settings':
                var.addon.openSettings()
            elif listItemAction == 'page_help':
                helpx.switch_to_page()
            elif listItemAction == 'addon_shutdown':
                dialog_close()
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'media_stop':
                xbmc.Player().stop()
            elif listItemAction == 'media_togglemute':
                xbmc.executebuiltin('Action(Mute)')
            elif listItemAction == 'media_fullscreen':
                var.PlayerCustom.Fullscreen(True)
            elif listItemAction == 'show_visualisation':
                radio.show_visualisation()
        elif clickId == 3001:
            dialog_close()
