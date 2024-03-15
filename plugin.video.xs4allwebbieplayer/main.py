import xbmc
import xbmcgui
import alarm
import apilogin
import cache
import dialog
import epg
import func
import getset
import guifunc
import helpx
import hybrid
import kids
import lifunc
import limain
import movies
import path
import player
import radio
import recorded
import recordingevent
import recordingfunc
import recordingseries
import search
import series
import settings
import sleep
import sport
import streamgenerate
import streamplay
import television
import threadfunc
import var
import vod
import widevine

def switch_to_page():
    if var.guiMain == None:
        var.guiMain = Gui('main.xml', var.addonpath, 'default', '720p')
        var.guiMain.setProperty('WebbiePlayerPage', 'Open')
        var.guiMain.doModal()
        var.guiMain = None

def close_the_page():
    if var.guiMain != None:
        #Stop currently playing media
        func.stop_playing_media()

        #Stop and reset all threads
        threadfunc.stop_reset_threads()

        #Close the shown window
        var.guiMain.close()

def dialog_close():
    if getset.setting_get('AfsluitschermOverslaan') == 'true':
        close_the_page()
    else:
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
            player.Fullscreen(True)
        else:
            var.guiMain.check_focus()

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Check if logged in on launch
        if var.ApiLoggedIn() == False:
            guifunc.updateLabelText(self, 1, "Aan het aanmelden.")
            apilogin.ApiLogin(False)

        #Update current login status
        if var.ApiLoggedIn() == True:
            guifunc.updateLabelText(self, 1, "Aangemeld, veel kijkplezier.")
        else:
            guifunc.updateLabelText(self, 1, "Aanmelden is mislukt.")

        #Add menu buttons to the page
        menuButtons = self.buttons_add_menu()

        #Add media buttons to the page
        self.buttons_add_media(False)

        #Focus on the menu buttons
        listContainer = self.getControl(1000)
        guifunc.controlFocus(self, listContainer)

        #Update the active alarms count
        self.count_alarm(True)

        #Update the recorded events count
        self.count_recorded_events()

        #Update the recording events count
        self.count_recording_events()

        #Update the recording series count
        self.count_recording_series()

        #Check if menu is already filled / prevent one time code
        if menuButtons == True:
            return

        #Check if Widevine is installed
        var.thread_check_requirements.Start(widevine.thread_check_requirements)

        #Load Webbie Player notification
        var.thread_notification.Start(self.thread_load_notification)

        #Check if user is logged in
        if var.ApiLoggedIn() == True:
            #Switch to last known television channel
            if getset.setting_get('StartWithLastChannel') == 'true' and getset.setting_get('StartWithKids') == 'false':
                self.switch_channel_currenttv()

            #Go to the desired page on startup
            if getset.setting_get('StartWithKids') == 'true':
                kids.switch_to_page()
            elif getset.setting_get('StartWithTelevision') == 'true':
                television.switch_to_page()

    def buttons_add_media(self, resetButtons):
        #Get and check the media control list container
        listContainer = self.getControl(1001)
        if resetButtons:
            guifunc.listReset(listContainer)
            listContainer = self.getControl(1000)
            guifunc.controlFocus(self, listContainer)
            return

        if xbmc.Player().isPlaying():
            #Add stop button
            if listContainer.size() == 0:
                listItem = xbmcgui.ListItem('Stop met afspelen')
                listItem.setProperty('ItemAction', 'media_stop')
                listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/stop.png'),'icon': path.resources('resources/skins/default/media/common/stop.png')})
                listContainer.addItem(listItem)

            #Add mute button
            if listContainer.size() == 1:
                listItem = xbmcgui.ListItem('On/demp het geluid')
                listItem.setProperty('ItemAction', 'media_togglemute')
                listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/volumemute.png'),'icon': path.resources('resources/skins/default/media/common/volumemute.png')})
                listContainer.addItem(listItem)

            #Add fullscreen button
            if xbmc.Player().isPlayingVideo():
                if listContainer.size() == 2:
                    listItem = xbmcgui.ListItem('Toon video speler')
                    listItem.setProperty('ItemAction', 'media_fullscreen')
                    listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/fullscreen.png'),'icon': path.resources('resources/skins/default/media/common/fullscreen.png')})
                    listContainer.addItem(listItem)
                elif listContainer.size() == 3:
                    updateItem = listContainer.getListItem(2)
                    updateItem.setLabel('Toon video speler')
                    updateItem.setProperty('ItemAction', 'media_fullscreen')
                    updateItem.setArt({'thumb': path.resources('resources/skins/default/media/common/fullscreen.png'),'icon': path.resources('resources/skins/default/media/common/fullscreen.png')})
            elif xbmc.Player().isPlayingAudio():
                if listContainer.size() == 2:
                    listItem = xbmcgui.ListItem('Toon visualisatie')
                    listItem.setProperty('ItemAction', 'show_visualisation')
                    listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/visualisation.png'),'icon': path.resources('resources/skins/default/media/common/visualisation.png')})
                    listContainer.addItem(listItem)
                elif listContainer.size() == 3:
                    updateItem = listContainer.getListItem(2)
                    updateItem.setLabel('Toon visualisatie')
                    updateItem.setProperty('ItemAction', 'show_visualisation')
                    updateItem.setArt({'thumb': path.resources('resources/skins/default/media/common/visualisation.png'),'icon': path.resources('resources/skins/default/media/common/visualisation.png')})
            elif listContainer.size() == 3:
                guifunc.listRemoveItem(listContainer, 2)
        else:
            guifunc.listReset(listContainer)
            listContainer = self.getControl(1000)
            guifunc.controlFocus(self, listContainer)

    def buttons_add_menu(self):
        #Get and check the main list container
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            return True

        #Add items to list container
        limain.list_load_combined(listContainer)

    def switch_channel_currenttv(self):
        ChannelId = getset.setting_get('CurrentChannelId', True)
        if func.string_isnullorempty(ChannelId) == False:
            ChannelListItem = streamgenerate.generate_listitem_tv(ChannelId)
            streamplay.play_tv(ChannelListItem, ShowInformation=True)

    def count_recorded_events(self):
        try:
            #Get and check the main list container
            listContainer = self.getControl(1000)
            if listContainer.size() == 0 or var.ApiLoggedIn() == False:
                return False

            #Load and count the planned recording
            recordingCount = recordingfunc.count_recorded_events()

            #Update the list count
            countItem = lifunc.search_listcontainer_label_listitem(listContainer, 'Bekijk Opnames')
            countItem.setLabel('Bekijk Opnames (' + str(recordingCount) + ')')
        except:
            pass

    def count_recording_events(self):
        try:
            #Get and check the main list container
            listContainer = self.getControl(1000)
            if listContainer.size() == 0 or var.ApiLoggedIn() == False:
                return False

            #Load and count the planned recording
            recordingCount = recordingfunc.count_recording_events()

            #Update the list count
            countItem = lifunc.search_listcontainer_label_listitem(listContainer, 'Geplande Opnames')
            countItem.setLabel('Geplande Opnames (' + str(recordingCount) + ')')
        except:
            pass

    def count_recording_series(self):
        try:
            #Get and check the main list container
            listContainer = self.getControl(1000)
            if listContainer.size() == 0 or var.ApiLoggedIn() == False:
                return False

            #Load and count the planned recording
            recordingCount = recordingfunc.count_recording_series()

            #Update the list count
            countItem = lifunc.search_listcontainer_label_listitem(listContainer, 'Geplande Series')
            countItem.setLabel('Geplande Series (' + str(recordingCount) + ')')
        except:
            pass

    def count_alarm(self, forceLoad=False):
        try:
            #Get and check the main list container
            listContainer = self.getControl(1000)
            if listContainer.size() == 0 or var.ApiLoggedIn() == False:
                return False

            #Load set program alarms
            alarm.alarm_json_load(forceLoad)

            #Update the list count
            countItem = lifunc.search_listcontainer_label_listitem(listContainer, 'Alarmen')
            countItem.setLabel('Alarmen (' + str(len(var.AlarmDataJson)) + ')')
        except:
            pass

    def thread_load_notification(self):
        try:
            #Set the download headers
            DownloadHeaders = {
                "User-Agent": getset.setting_get('CustomUserAgent')
            }

            #Download notification message
            RequestUrl = str(path.requirements()) + 'notification.txt'
            DownloadRequest = hybrid.urllib_request(RequestUrl, headers=DownloadHeaders)
            DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
            DownloadDataString = DownloadDataHttp.read().decode()

            #Set notification message
            guifunc.updateLabelText(self, 2, DownloadDataString)
        except:
            pass

    def check_focus(self):
        focusMain = xbmc.getCondVisibility('Control.HasFocus(1000)')
        focusNavigation = xbmc.getCondVisibility('Control.HasFocus(1001)')
        if focusNavigation == True:
            focusControl = self.getControl(1001)
            guifunc.controlFocus(self, focusControl)
        elif focusMain == True:
            focusControl = self.getControl(1000)
            guifunc.controlFocus(self, focusControl)

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            dialog_close()

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'page_television':
                television.switch_to_page()
            elif listItemAction == 'page_radio':
                radio.switch_to_page()
            elif listItemAction == 'page_vod':
                vod.switch_to_page()
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
            elif listItemAction == 'cache_remove_all':
                cache.cache_remove_all()
            elif listItemAction == 'addon_settings':
                settings.open_settings()
            elif listItemAction == 'page_help':
                helpx.switch_to_page()
            elif listItemAction == 'addon_shutdown':
                dialog_close()
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'media_stop':
                xbmc.executebuiltin('PlayerControl(Stop)')
            elif listItemAction == 'media_togglemute':
                xbmc.executebuiltin('Action(Mute)')
            elif listItemAction == 'media_fullscreen':
                player.Fullscreen(True)
            elif listItemAction == 'show_visualisation':
                player.Fullscreen(True)
        elif clickId == 3001:
            dialog_close()
