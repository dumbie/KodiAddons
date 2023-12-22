import xbmc
import xbmcgui
import dialog
import download
import epg
import files
import func
import path
import likidsepisodeweek
import likidsepisodevod
import likidsprogramweek
import likidsprogramvod
import searchdialog
import stream
import var

def switch_to_page():
    if var.guiKids == None:
        var.guiKids = Gui('series.xml', var.addonpath, 'default', '720p')
        var.guiKids.show()

def close_the_page():
    if var.guiKids != None:
        #Check kids page lock
        if lock_check_page() == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kidstongue.png')
            xbmcgui.Dialog().notification(var.addonname, "Helaas pindakaas!", notificationIcon, 2500, False)
            return False

        #Save select index
        var.guiKids.save_select_index()

        #Close the shown window
        var.guiKids.close()
        var.guiKids = None
        return True

def lock_check_hidden():
    if var.addon.getSetting('KidsHiddenLock') == 'true':
        return lock_check_dialog()
    else:
        return True

def lock_check_page():
    if var.addon.getSetting('KidsPageLock') == 'true':
        return lock_check_dialog()
    else:
        return True

def lock_check_dialog():
    #Keyboard enter kids pincode
    keyboard = xbmc.Keyboard('default', 'heading')
    keyboard.setHeading('Kids pincode')
    keyboard.setDefault('')
    keyboard.setHiddenInput(True)
    keyboard.doModal()
    if keyboard.isConfirmed() == True:
        return str(var.addon.getSetting('KidsPincode')) == keyboard.getText()
    return False

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        func.updateLabelText(self, 3, "Kids")
        self.update_kids_background()
        self.buttons_add_navigation()
        self.load_program(False, False, var.KidsProgramSelectIndex, var.KidsEpisodeSelectIndex)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'load_episodes_vod':
                self.load_episodes_vod(listItemSelected, True)
            elif listItemAction == 'load_episodes_week':
                self.load_episodes_week(listItemSelected, True)
            elif listItemAction == 'play_episode_week':
                stream.play_stream_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'refresh_program':
                self.load_program(True, True)
        elif clickId == 1002:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'play_episode_vod':
                stream.play_stream_vod(listItemSelected, False)
            elif listItemAction == 'play_episode_week':
                stream.play_stream_program(listItemSelected, False)
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
        focusEpisodesList = xbmc.getCondVisibility('Control.HasFocus(1002)')
        focusEpisodesScroll = xbmc.getCondVisibility('Control.HasFocus(2002)')
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            if focusEpisodesList == False and focusEpisodesScroll == False:
                close_the_page()
            else:
                listcontainer = self.getControl(1000)
                self.setFocus(listcontainer)
                xbmc.sleep(100)
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_program()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusEpisodesList:
            self.open_context_menu()

    def save_select_index(self):
        listContainer = self.getControl(1000)
        var.KidsProgramSelectIndex = listContainer.getSelectedPosition()

        listContainer = self.getControl(1002)
        var.KidsEpisodeSelectIndex = listContainer.getSelectedPosition()

    def open_context_menu(self):
        listcontainer = self.getControl(1002)
        listItemSelected = listcontainer.getSelectedItem()
        programWeek = listItemSelected.getProperty("ProgramWeek")
        if programWeek == 'true':
            dialogAnswers = ['Aflevering in de TV Gids tonen']
            dialogHeader = 'Aflevering Menu'
            dialogSummary = 'Wat wilt u doen met de geselecteerde aflevering?'
            dialogFooter = ''

            dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
            if dialogResult == 'Aflevering in de TV Gids tonen':
                var.EpgNavigateProgramId = listItemSelected.getProperty("ProgramId")
                var.EpgCurrentChannelId = listItemSelected.getProperty("ChannelId")
                var.EpgCurrentLoadDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
                if close_the_page() == True:
                    xbmc.sleep(100)
                    epg.switch_to_page()

    def update_kids_background(self):
        if files.existFile(path.addonstorage("background.png")) == False:
            func.updateImage(self, 8000, 'common/background_addon_kids.png')

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Zoek programma")
        listitem.setProperty('Action', 'search_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Vernieuwen")
        listitem.setProperty('Action', 'refresh_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek programma')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchChannelTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_program(True, False)
        var.SearchChannelTerm = ''

    def load_episodes_vod(self, listItem, selectList=False, selectIndex=0):
        #Get the selected parentid
        selectedParentId = listItem.getProperty('ProgramId')
        selectedSeriesName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listcontainer = self.getControl(1002)
        listcontainer.reset()

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen downloaden')

        #Download the series episodes
        seasonDownloaded = download.download_series_season(selectedParentId)
        if seasonDownloaded == None:
            func.updateLabelText(self, 2, 'Afleveringen niet beschikbaar')
            return False

        func.updateLabelText(self, 2, 'Afleveringen laden')

        #Add items to sort list
        listcontainersort = []
        likidsepisodevod.list_load(listcontainersort, seasonDownloaded, selectedSeriesName, selectedPictureUrl)

        #Sort and add items to container
        listcontainer.addItems(listcontainersort)

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listcontainer.size()) + ' afleveringen)')

        if listcontainer.size() > 0:
            #Focus list container
            if selectList == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)

            #Select list item
            listcontainer.selectItem(selectIndex)
            xbmc.sleep(100)

    def load_episodes_week(self, listItem, selectList=False, selectIndex=0):
        #Get the selected parentid
        selectedSeriesName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listcontainer = self.getControl(1002)
        listcontainer.reset()
        listcontainersort = []

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen laden')

        #Process all the episodes
        likidsepisodeweek.list_load(listcontainersort, selectedSeriesName, selectedPictureUrl)

        #Sort and add episodes to the list
        listcontainersort.sort(key=lambda x: (int(x.getProperty('ProgramSeasonInt')), int(x.getProperty('ProgramEpisodeInt'))))
        listcontainer.addItems(listcontainersort)

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listcontainer.size()) + ' afleveringen)')

        if listcontainer.size() > 0:
            #Focus list container
            if selectList == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)

            #Select list item
            listcontainer.selectItem(selectIndex)
            xbmc.sleep(100)

    def load_program(self, forceLoad=False, forceUpdate=False, programSelectIndex=0, episodeSelectIndex=0):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, "Programma's worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0: return True
        else:
            listcontainer.reset()

        #Download the programs
        func.updateLabelText(self, 1, "Programma's downloaden")
        downloadResult = download.download_vod_series_kids(forceUpdate)
        downloadResultWeek = download.download_search_kids(forceUpdate)
        if downloadResult == False or downloadResultWeek == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, "Programma's laden")

        #Add items to sort list
        listcontainersort = []
        likidsprogramweek.list_load(listcontainersort)
        likidsprogramvod.list_load(listcontainersort)

        #Sort and add items to container
        listcontainersort.sort(key=lambda x: x.getProperty('ProgramName'))
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_program(True, programSelectIndex)

        #Load selected episodes
        listItemSelected = listcontainer.getSelectedItem()
        listItemAction = listItemSelected.getProperty('Action')
        if listItemAction == 'load_episodes_vod':
            self.load_episodes_vod(listItemSelected, False, episodeSelectIndex)
        elif listItemAction == 'load_episodes_week':
            self.load_episodes_week(listItemSelected, False, episodeSelectIndex)

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            func.updateVisibility(self, 2, True)
            func.updateVisibility(self, 3002, True)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 4, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's")
                func.updateLabelText(self, 4, "")

            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(selectIndex)
                xbmc.sleep(100)
        else:
            func.updateVisibility(self, 2, False)
            func.updateVisibility(self, 3002, False)
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 4, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 4, "")
                listcontainer.selectItem(0)
            xbmc.sleep(100)
