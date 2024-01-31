import xbmc
import xbmcgui
import dialog
import download
import epg
import files
import func
import lifunc
import path
import likidsepisodeweek
import likidsepisodevod
import likidsprogramweek
import likidsprogramvod
import searchdialog
import streamplay
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

def source_plugin_list_program():
    downloadResult = download.download_vod_kids()
    downloadResultWeek = download.download_search_kids()
    #if downloadResult == False or downloadResultWeek == False:

    #Add items to sort list
    listContainerSort = []
    likidsprogramweek.list_load(listContainerSort)
    likidsprogramvod.list_load(listContainerSort)

    #Sort items in list
    listContainerSort.sort(key=lambda x: x.getProperty('ProgramName'))

    #Add items to container
    for listItem in listContainerSort:
        ListAction = str(listItem.getProperty('Action'))
        ProgramId = listItem.getProperty('ProgramId')
        ProgramName = listItem.getProperty('ProgramName')
        PictureUrl = listItem.getProperty('PictureUrl')
        ItemIsFolder = ListAction.startswith('play_stream') == False
        lifunc.auto_add_item(listItem, None, dirUrl=ListAction+'='+ProgramId+var.splitchar+ProgramName+var.splitchar+PictureUrl, dirFolder=ItemIsFolder)
    lifunc.auto_end_items()

def source_plugin_list_episode_vod(ProgramId, PictureUrl):
    seasonDownloaded = download.download_series_season(ProgramId)
    #if seasonDownloaded == None:
    likidsepisodevod.list_load(None, seasonDownloaded, PictureUrl)

def source_plugin_list_episode_week(ProgramName, PictureUrl):
    downloadResultWeek = download.download_search_kids()
    likidsepisodeweek.list_load(None, ProgramName, PictureUrl)

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
            if listItemAction == 'load_kids_episodes_vod':
                self.load_kids_episodes_vod(listItemSelected, True)
            elif listItemAction == 'load_kids_episodes_week':
                self.load_kids_episodes_week(listItemSelected, True)
            elif listItemAction == 'play_stream_program':
                streamplay.play_program(listItemSelected, False)
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
            if listItemAction == 'play_stream_vod':
                streamplay.play_vod(listItemSelected, False)
            elif listItemAction == 'play_stream_program':
                streamplay.play_program(listItemSelected, False)
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
        focusEpisodesList = xbmc.getCondVisibility('Control.HasFocus(1002)')
        focusEpisodesScroll = xbmc.getCondVisibility('Control.HasFocus(2002)')
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            if focusEpisodesList == False and focusEpisodesScroll == False:
                close_the_page()
            else:
                listContainer = self.getControl(1000)
                self.setFocus(listContainer)
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
        listContainer = self.getControl(1002)
        listItemSelected = listContainer.getSelectedItem()
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
        listContainer = self.getControl(1001)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga een stap terug')
        listItem.setProperty('Action', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Zoek programma")
        listItem.setProperty('Action', 'search_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Vernieuwen")
        listItem.setProperty('Action', 'refresh_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listContainer.addItem(listItem)

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

    def load_kids_episodes_vod(self, listItem, selectList=False, selectIndex=0):
        #Get the selected parentid
        selectedParentId = listItem.getProperty('ProgramId')
        selectedSeriesName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listContainer = self.getControl(1002)
        listContainer.reset()

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen downloaden')

        #Download the series episodes
        seasonDownloaded = download.download_series_season(selectedParentId)
        if seasonDownloaded == None:
            func.updateLabelText(self, 2, 'Afleveringen niet beschikbaar')
            return False

        func.updateLabelText(self, 2, 'Afleveringen laden')

        #Add items to sort list
        listContainerSort = []
        likidsepisodevod.list_load(listContainerSort, seasonDownloaded, selectedPictureUrl)

        #Sort and add items to container
        listContainer.addItems(listContainerSort)

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listContainer.size()) + ' afleveringen)')

        if listContainer.size() > 0:
            #Focus list container
            if selectList == True:
                self.setFocus(listContainer)
                xbmc.sleep(100)

            #Select list item
            listContainer.selectItem(selectIndex)
            xbmc.sleep(100)

    def load_kids_episodes_week(self, listItem, selectList=False, selectIndex=0):
        #Get the selected parentid
        selectedSeriesName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listContainer = self.getControl(1002)
        listContainer.reset()
        listContainerSort = []

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen laden')

        #Process all the episodes
        likidsepisodeweek.list_load(listContainerSort, selectedSeriesName, selectedPictureUrl)

        #Sort and add episodes to the list
        listContainerSort.sort(key=lambda x: (int(x.getProperty('ProgramSeasonInt')), int(x.getProperty('ProgramEpisodeInt'))))
        listContainer.addItems(listContainerSort)

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listContainer.size()) + ' afleveringen)')

        if listContainer.size() > 0:
            #Focus list container
            if selectList == True:
                self.setFocus(listContainer)
                xbmc.sleep(100)

            #Select list item
            listContainer.selectItem(selectIndex)
            xbmc.sleep(100)

    def load_program(self, forceLoad=False, forceUpdate=False, programSelectIndex=0, episodeSelectIndex=0):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, "Programma's worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listContainer.size() > 0: return True
        else:
            listContainer.reset()

        #Download the programs
        func.updateLabelText(self, 1, "Programma's downloaden")
        downloadResult = download.download_vod_kids(forceUpdate)
        downloadResultWeek = download.download_search_kids(forceUpdate)
        if downloadResult == False or downloadResultWeek == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            listContainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, "Programma's laden")

        #Add items to sort list
        listContainerSort = []
        likidsprogramweek.list_load(listContainerSort)
        likidsprogramvod.list_load(listContainerSort)

        #Sort and add items to container
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramName'))
        listContainer.addItems(listContainerSort)

        #Update the status
        self.count_program(True, programSelectIndex)

        #Load selected episodes
        listItemSelected = listContainer.getSelectedItem()
        listItemAction = listItemSelected.getProperty('Action')
        if listItemAction == 'load_kids_episodes_vod':
            self.load_kids_episodes_vod(listItemSelected, False, episodeSelectIndex)
        elif listItemAction == 'load_kids_episodes_week':
            self.load_kids_episodes_week(listItemSelected, False, episodeSelectIndex)

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            func.updateVisibility(self, 2, True)
            func.updateVisibility(self, 3002, True)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, str(listContainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 4, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
            else:
                func.updateLabelText(self, 1, str(listContainer.size()) + " programma's")
                func.updateLabelText(self, 4, "")

            if resetSelect == True:
                self.setFocus(listContainer)
                xbmc.sleep(100)
                listContainer.selectItem(selectIndex)
                xbmc.sleep(100)
        else:
            func.updateVisibility(self, 2, False)
            func.updateVisibility(self, 3002, False)
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 4, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
                listContainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 4, "")
                listContainer.selectItem(0)
            xbmc.sleep(100)
