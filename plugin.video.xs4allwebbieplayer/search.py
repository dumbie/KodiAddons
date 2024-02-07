import xbmc
import xbmcgui
import dialog
import download
import epg
import func
import lisearch
import path
import searchdialog
import streamplay
import var

def switch_to_page():
    if var.guiSearch == None:
        var.guiSearch = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiSearch.show()

def close_the_page():
    if var.guiSearch != None:
        #Save select index
        var.guiSearch.save_select_index()

        #Close the shown window
        var.guiSearch.close()
        var.guiSearch = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Prepare the search page
        func.updateLabelText(self, 2, "Terugzoeken")
        self.buttons_add_navigation()
        listContainer = self.getControl(1000)
        if listContainer.size() == 0:
            if var.SearchProgramDataJson == []:
                func.updateLabelText(self, 1, 'Geen zoek term')
                listContainer = self.getControl(1001)
                self.setFocus(listContainer)
                xbmc.sleep(100)
                listContainer.selectItem(1)
                xbmc.sleep(100)
            else:
                self.search_list(var.SearchSelectIndex)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'play_stream':
                streamplay.play_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'search_result':
                self.search_result()
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
        focusItem = xbmc.getCondVisibility('Control.HasFocus(1000)')
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_program()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusItem:
            self.open_context_menu()

    def save_select_index(self):
        listContainer = self.getControl(1000)
        var.SearchSelectIndex = listContainer.getSelectedPosition()

    def open_context_menu(self):
        dialogAnswers = ['Programma zoeken in resultaat', 'Programma in de TV Gids tonen']
        dialogHeader = 'Programma Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma zoeken in resultaat':
            listContainer = self.getControl(1000)
            listItemSelected = listContainer.getSelectedItem()
            ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

            #Set search filter term
            var.SearchTermCurrent = func.search_filter_string(ProgramNameRaw)
            self.search_list()
            var.SearchTermCurrent = ''
        elif dialogResult == 'Programma in de TV Gids tonen':
            listContainer = self.getControl(1000)
            listItemSelected = listContainer.getSelectedItem()
            var.EpgNavigateProgramId = listItemSelected.getProperty("ProgramId")
            var.EpgCurrentChannelId = listItemSelected.getProperty("ChannelId")
            var.EpgCurrentLoadDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
            close_the_page()
            xbmc.sleep(100)
            epg.switch_to_page()

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

        listItem = xbmcgui.ListItem("Zoek in resultaat")
        listItem.setProperty('Action', 'search_result')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/searchresult.png'), 'icon': path.resources('resources/skins/default/media/common/searchresult.png')})
        listContainer.addItem(listItem)

    def search_result(self):
        #Check if search result is available
        if var.SearchProgramDataJson == []:
            notificationIcon = path.resources('resources/skins/default/media/common/searchresult.png')
            xbmcgui.Dialog().notification(var.addonname, 'Geen zoekresultaten.', notificationIcon, 2500, False)
            return

        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek in resultaat')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchTermCurrent = func.search_filter_string(searchDialogTerm.string)
        self.search_list()
        var.SearchTermCurrent = ''

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek programma')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return True

        #Check the search term
        if func.string_isnullorempty(searchDialogTerm.string) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/search.png')
            xbmcgui.Dialog().notification(var.addonname, 'Leeg zoek term', notificationIcon, 2500, False)
            return True

        #Download the search programs
        func.updateLabelText(self, 1, "Zoek resultaat downloaden")
        downloadResult = download.download_search_program(searchDialogTerm.string)
        if downloadResult == None:
            func.updateLabelText(self, 1, 'Zoeken mislukt')
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            listContainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Update search result
        var.SearchDownloadSearchTerm = searchDialogTerm.string
        var.SearchProgramDataJson = downloadResult

        #List search results
        self.search_list()

    def search_list(self, selectIndex=0):
        #Get and check the list container
        listContainer = self.getControl(1000)
        listContainer.reset()

        #Add items to list container
        func.updateLabelText(self, 1, "Zoek resultaat laden")
        lisearch.list_load_combined(listContainer)

        #Update the status
        self.count_program(True, selectIndex)

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            func.updateLabelText(self, 1, str(listContainer.size()) + " zoekresultaten")
            if func.string_isnullorempty(var.SearchTermCurrent):
                func.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchDownloadSearchTerm)
            else:
                func.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchTermCurrent + " [COLOR gray]in[/COLOR] " + var.SearchDownloadSearchTerm)
            if resetSelect == True:
                self.setFocus(listContainer)
                xbmc.sleep(100)
                listContainer.selectItem(selectIndex)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 1, "Geen zoekresultaten")
            if func.string_isnullorempty(var.SearchTermCurrent):
                func.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchDownloadSearchTerm)
            else:
                func.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchTermCurrent + " [COLOR gray]in[/COLOR] " + var.SearchDownloadSearchTerm)

            #Focus on menu
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            if var.SearchTermCurrent != '':
                listContainer.selectItem(2)
            else:
                listContainer.selectItem(1)
            xbmc.sleep(100)
