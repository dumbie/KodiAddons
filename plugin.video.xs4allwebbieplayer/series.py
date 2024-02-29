import xbmc
import xbmcgui
import dialog
import epg
import func
import guifunc
import liseriesepisode
import liseriesprogram
import path
import player
import searchdialog
import streamplay
import var

def switch_to_page():
    if var.guiSeries == None:
        var.guiSeries = Gui('series.xml', var.addonpath, 'default', '720p')
        var.guiSeries.setProperty('WebbiePlayerPage', 'Open')
        var.guiSeries.show()

def close_the_page():
    if var.guiSeries != None:
        #Save select index
        var.guiSeries.save_select_index()

        #Close the shown window
        var.guiSeries.close()
        var.guiSeries = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        guifunc.updateLabelText(self, 3, "Series")
        self.buttons_add_navigation()
        self.load_program(False, False, var.SeriesProgramSelectIndex, var.SeriesEpisodeSelectIndex)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'load_series_episodes_vod':
                self.load_episodes_vod(listItemSelected, True)
            elif listItemAction == 'load_series_episodes_program':
                self.load_episodes_program(listItemSelected, True)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'refresh_programs':
                self.load_program(True, True)
        elif clickId == 1002:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'play_stream_vod':
                streamplay.play_vod(listItemSelected, False)
            elif listItemAction == 'play_stream_program':
                streamplay.play_program(listItemSelected, False)
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
        focusEpisodesList = xbmc.getCondVisibility('Control.HasFocus(1002)')
        focusEpisodesScroll = xbmc.getCondVisibility('Control.HasFocus(2002)')
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            if focusEpisodesList == False and focusEpisodesScroll == False:
                close_the_page()
            else:
                listContainer = self.getControl(1000)
                guifunc.controlFocus(self, listContainer)
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
        var.SeriesProgramSelectIndex = listContainer.getSelectedPosition()

        listContainer = self.getControl(1002)
        var.SeriesEpisodeSelectIndex = listContainer.getSelectedPosition()

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
                close_the_page()
                epg.switch_to_page()

    def buttons_add_navigation(self):
        listContainer = self.getControl(1001)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga een stap terug')
        listItem.setProperty('ItemAction', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Zoek naar serie")
        listItem.setProperty('ItemAction', 'search_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Vernieuwen")
        listItem.setProperty('ItemAction', 'refresh_programs')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listContainer.addItem(listItem)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek naar serie')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchTermCurrent = func.search_filter_string(searchDialogTerm.string)
        self.load_program(True, False)
        var.SearchTermCurrent = ''

    def load_episodes_vod(self, listItem, focusList=False, selectIndex=0):
        #Get the selected parentid
        selectedProgramId = listItem.getProperty('ProgramId')
        selectedProgramName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listContainer = self.getControl(1002)
        guifunc.listReset(listContainer)

        #Update the episodes status
        guifunc.updateLabelText(self, 2, 'Afleveringen laden')

        #Add items to sort list
        if liseriesepisode.list_load_vod_combined(selectedProgramId, selectedPictureUrl, listContainer) == False:
            guifunc.updateLabelText(self, 2, 'Afleveringen niet beschikbaar')
            return False

        #Update the episodes status
        guifunc.updateLabelText(self, 2, selectedProgramName + ' (' + str(listContainer.size()) + ' afleveringen)')

        if listContainer.size() > 0:
            #Focus list container
            if focusList == True:
                guifunc.controlFocus(self, listContainer)

            #Select list item
            guifunc.listSelectItem(listContainer, selectIndex)

    def load_episodes_program(self, listItem, focusList=False, selectIndex=0):
        #Get the selected parentid
        selectedProgramName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listContainer = self.getControl(1002)
        guifunc.listReset(listContainer)

        #Update the episodes status
        guifunc.updateLabelText(self, 2, 'Afleveringen laden')

        #Add items to sort list
        if liseriesepisode.list_load_program_combined(selectedProgramName, selectedPictureUrl, listContainer) == False:
            guifunc.updateLabelText(self, 2, 'Afleveringen niet beschikbaar')
            return False

        #Update the episodes status
        guifunc.updateLabelText(self, 2, selectedProgramName + ' (' + str(listContainer.size()) + ' afleveringen)')

        if listContainer.size() > 0:
            #Focus list container
            if focusList == True:
                guifunc.controlFocus(self, listContainer)

            #Select list item
            guifunc.listSelectItem(listContainer, selectIndex)

    def load_program(self, forceLoad=False, forceUpdate=False, programSelectIndex=0, episodeSelectIndex=0):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, "Series worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listContainer.size() > 0: return True
        else:
            guifunc.listReset(listContainer)

        #Add items to list container
        guifunc.updateLabelText(self, 1, "Series laden")
        guifunc.updateLabelText(self, 4, "")
        if liseriesprogram.list_load_combined(listContainer, forceUpdate) == False:
            guifunc.updateLabelText(self, 1, 'Niet beschikbaar')
            guifunc.updateLabelText(self, 4, "")
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectItem(listContainer, 0)
            return False

        #Update the status
        self.count_program(True, programSelectIndex)

        #Load selected episodes
        listItemSelected = listContainer.getSelectedItem()
        listItemAction = listItemSelected.getProperty('ItemAction')
        if listItemAction == 'load_series_episodes_vod':
            self.load_episodes_vod(listItemSelected, False, episodeSelectIndex)
        elif listItemAction == 'load_series_episodes_program':
            self.load_episodes_program(listItemSelected, False, episodeSelectIndex)

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            guifunc.updateVisibility(self, 2, True)
            guifunc.updateVisibility(self, 3002, True)
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " series gevonden")
                guifunc.updateLabelText(self, 4, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchTermCurrent)
            else:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " series")
                guifunc.updateLabelText(self, 4, "")

            if resetSelect == True:
                guifunc.controlFocus(self, listContainer)
                guifunc.listSelectItem(listContainer, selectIndex)
        else:
            guifunc.updateVisibility(self, 2, False)
            guifunc.updateVisibility(self, 3002, False)
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                guifunc.updateLabelText(self, 1, "Geen series gevonden")
                guifunc.updateLabelText(self, 4, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchTermCurrent)
                guifunc.listSelectItem(listContainer, 1)
            else:
                guifunc.updateLabelText(self, 1, "Geen series")
                guifunc.updateLabelText(self, 4, "")
                guifunc.listSelectItem(listContainer, 0)
