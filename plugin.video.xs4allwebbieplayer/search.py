import xbmc
import xbmcgui
import dialog
import epg
import func
import guifunc
import lisearch
import path
import player
import searchdialog
import streamplay
import var

def switch_to_page():
    if var.guiSearch == None:
        var.guiSearch = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiSearch.setProperty('WebbiePlayerPage', 'Open')
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
        guifunc.updateLabelText(self, 2, "Terugzoeken")
        self.buttons_add_navigation()
        listContainer = self.getControl(1000)
        if listContainer.size() == 0:
            if func.string_isnullorempty(var.SearchTermDownload) == True:
                guifunc.updateLabelText(self, 1, 'Geen zoek term')
                guifunc.updateLabelText(self, 3, "")
                listContainer = self.getControl(1001)
                guifunc.controlFocus(self, listContainer)
                guifunc.listSelectItem(listContainer, 1)
            else:
                self.search_list(False, var.SearchSelectIndex)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'play_stream_program':
                streamplay.play_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'search_result':
                self.search_result()
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
            self.search_program_result()
        elif dialogResult == 'Programma in de TV Gids tonen':
            self.program_show_in_epg()

    def program_show_in_epg(self):
        listContainer = self.getControl(1000)
        listItemSelected = listContainer.getSelectedItem()
        var.EpgNavigateProgramId = listItemSelected.getProperty("ProgramId")
        var.EpgCurrentChannelId = listItemSelected.getProperty("ChannelId")
        var.EpgCurrentLoadDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
        close_the_page()
        epg.switch_to_page()

    def search_program_result(self):
        listContainer = self.getControl(1000)
        listItemSelected = listContainer.getSelectedItem()
        ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

        #Set search filter term
        var.SearchTermResult = func.search_filter_string(ProgramNameRaw)
        self.search_list(False)
        var.SearchTermResult = ''

    def buttons_add_navigation(self):
        listContainer = self.getControl(1001)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga een stap terug')
        listItem.setProperty('ItemAction', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Zoek programma")
        listItem.setProperty('ItemAction', 'search_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Zoek in resultaat")
        listItem.setProperty('ItemAction', 'search_result')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/searchresult.png'), 'icon': path.resources('resources/skins/default/media/common/searchresult.png')})
        listContainer.addItem(listItem)

    def search_result(self):
        #Check if search result is available
        if var.SearchProgramDataJson == []:
            notificationIcon = path.resources('resources/skins/default/media/common/searchresult.png')
            xbmcgui.Dialog().notification(var.addonname, 'Geen zoekresultaten.', notificationIcon, 2500, False)
            return

        #Open search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek in resultaat')

        #Check search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchTermResult = func.search_filter_string(searchDialogTerm.string)
        self.search_list(False)
        var.SearchTermResult = ''

    def search_program(self):
        #Open search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek programma')

        #Check search term
        if searchDialogTerm.cancelled == True:
            return

        #Check search term
        if func.string_isnullorempty(searchDialogTerm.string) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/search.png')
            xbmcgui.Dialog().notification(var.addonname, 'Leeg zoek term', notificationIcon, 2500, False)
            return

        #Update search term
        var.SearchTermDownload = searchDialogTerm.string

        #List search results
        self.search_list(True)

    def search_list(self, forceUpdate=True, selectIndex=0):
        #Get and check the list container
        listContainer = self.getControl(1000)
        guifunc.listReset(listContainer)

        #Add items to list container
        guifunc.updateLabelText(self, 1, "Zoek resultaat laden")
        guifunc.updateLabelText(self, 3, "")
        if lisearch.list_load_combined(listContainer, forceUpdate) == False:
            guifunc.updateLabelText(self, 1, 'Zoeken mislukt')
            guifunc.updateLabelText(self, 3, "")
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectItem(listContainer, 0)
            return False

        #Update the status
        self.count_program(True, selectIndex)

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            guifunc.updateLabelText(self, 1, str(listContainer.size()) + " zoekresultaten")
            if func.string_isnullorempty(var.SearchTermResult):
                guifunc.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchTermDownload)
            else:
                guifunc.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchTermResult + " [COLOR gray]in[/COLOR] " + var.SearchTermDownload)
            if resetSelect == True:
                guifunc.controlFocus(self, listContainer)
                guifunc.listSelectItem(listContainer, selectIndex)
        else:
            guifunc.updateLabelText(self, 1, "Geen zoekresultaten")
            if func.string_isnullorempty(var.SearchTermResult):
                guifunc.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchTermDownload)
            else:
                guifunc.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchTermResult + " [COLOR gray]in[/COLOR] " + var.SearchTermDownload)

            #Focus on menu
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.listSelectItem(listContainer, 2)
            else:
                guifunc.listSelectItem(listContainer, 1)
