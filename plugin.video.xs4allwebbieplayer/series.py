import xbmc
import xbmcgui
import dialog
import download
import epg
import func
import path
import program.seriesepisodeweek
import program.seriesepisodevod
import program.seriesprogramweek
import program.seriesprogramvod
import searchdialog
import stream
import var

def switch_to_page():
    if var.guiSeries == None:
        var.guiSeries = Gui('series.xml', var.addonpath, 'default', '720p')
        var.guiSeries.show()

def close_the_page():
    if var.guiSeries != None:
        #Close the shown window
        var.guiSeries.close()
        var.guiSeries = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        func.updateLabelText(self, 3, "Series")
        self.buttons_add_navigation()
        self.load_series(False, False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'load_episodes_vod':
                self.load_episodes_vod(listItemSelected, True)
            elif listItemAction == 'load_episodes_week':
                self.load_episodes_week(listItemSelected, True)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_serie':
                self.search_serie()
            elif listItemAction == 'refresh_program':
                self.load_series(True, True)
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
            self.search_serie()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusEpisodesList:
            self.open_context_menu()

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
                close_the_page()
                xbmc.sleep(100)
                epg.switch_to_page()

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Zoek naar serie")
        listitem.setProperty('Action', 'search_serie')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Vernieuwen")
        listitem.setProperty('Action', 'refresh_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def search_serie(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek naar serie')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_series(True, False)
        var.SearchFilterTerm = ''

    def load_episodes_vod(self, listItem, selectList=False):
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

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen laden')

        #Process all the episodes
        program.seriesepisodevod.list_load(listcontainer, seasonDownloaded, selectedSeriesName, selectedPictureUrl)

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listcontainer.size()) + ' afleveringen)')

        #Select the list container
        if selectList == True and listcontainer.size() > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)

    def load_episodes_week(self, listItem, selectList=False):
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
        program.seriesepisodeweek.list_load(listcontainersort, selectedSeriesName, selectedPictureUrl)

        #Sort and add episodes to the list
        listcontainersort.sort(key=lambda x: (int(x.getProperty('ProgramSeasonInt')), int(x.getProperty('ProgramEpisodeInt'))))
        listcontainer.addItems(listcontainersort)

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listcontainer.size()) + ' afleveringen)')

        #Select the list container
        if selectList == True and listcontainer.size() > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)

    def load_series(self, forceLoad=False, forceUpdate=False):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, "Series worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0: return True
        else:
            listcontainer.reset()

        #Download the series
        func.updateLabelText(self, 1, "Series downloaden")
        downloadResult = download.download_vod_series(forceUpdate)
        downloadResultWeek = download.download_search_series(forceUpdate)
        if downloadResult == False or downloadResultWeek == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Add series to the list
        func.updateLabelText(self, 1, "Series laden")
        listcontainersort = []
        program.seriesprogramweek.list_load(listcontainersort)
        program.seriesprogramvod.list_load(listcontainersort)

        #Sort and add programs to the list
        listcontainersort.sort(key=lambda x: x.getProperty('ProgramName'))
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_series(True)

        #Load selected episodes
        listItemSelected = listcontainer.getSelectedItem()
        listItemAction = listItemSelected.getProperty('Action')
        if listItemAction == 'load_episodes_vod':
            self.load_episodes_vod(listItemSelected, False)
        elif listItemAction == 'load_episodes_week':
            self.load_episodes_week(listItemSelected, False)

    #Update the status
    def count_series(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            func.updateVisibility(self, 2, True)
            func.updateVisibility(self, 3002, True)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " series gevonden")
                func.updateLabelText(self, 4, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchFilterTerm)
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " series")
                func.updateLabelText(self, 4, "")

            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateVisibility(self, 2, False)
            func.updateVisibility(self, 3002, False)
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, "Geen series gevonden")
                func.updateLabelText(self, 4, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchFilterTerm)
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, "Geen series")
                func.updateLabelText(self, 4, "")
                listcontainer.selectItem(0)
            xbmc.sleep(100)
