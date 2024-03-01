import xbmc
import xbmcgui
import dialog
import epg
import func
import guifunc
import limovies
import path
import player
import searchdialog
import streamplay
import var

def switch_to_page():
    if var.guiMovies == None:
        var.guiMovies = Gui('movies.xml', var.addonpath, 'default', '720p')
        var.guiMovies.setProperty('WebbiePlayerPage', 'Open')
        var.guiMovies.show()

def close_the_page():
    if var.guiMovies != None:
        #Save select index
        var.guiMovies.save_select_index()

        #Close the shown window
        var.guiMovies.close()
        var.guiMovies = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        self.buttons_add_navigation()
        self.load_movies(False, False, var.MovieSelectIndex)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'play_stream_vod':
                streamplay.play_vod(listItemSelected, False)
            elif listItemAction == 'play_stream_program':
                streamplay.play_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'refresh_programs':
                self.load_movies(True, True)
            elif listItemAction == 'search_movie':
                self.search_movie()
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
            self.search_movie()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusItem:
            self.open_context_menu()

    def save_select_index(self):
        listContainer = self.getControl(1000)
        var.MovieSelectIndex = listContainer.getSelectedPosition()

    def open_context_menu(self):
        listContainer = self.getControl(1000)
        listItemSelected = listContainer.getSelectedItem()
        programWeek = listItemSelected.getProperty("ProgramWeek")
        if programWeek == 'true':
            dialogAnswers = ['Film in de TV Gids tonen']
            dialogHeader = 'Film Menu'
            dialogSummary = 'Wat wilt u doen met de geselecteerde film?'
            dialogFooter = ''

            dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
            if dialogResult == 'Film in de TV Gids tonen':
                self.program_show_in_epg(listItemSelected)

    def program_show_in_epg(self, listItemSelected):
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

        listItem = xbmcgui.ListItem("Zoek naar film")
        listItem.setProperty('ItemAction', 'search_movie')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Vernieuwen")
        listItem.setProperty('ItemAction', 'refresh_programs')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listContainer.addItem(listItem)

    def search_movie(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek naar film')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchTermResult = func.search_filter_string(searchDialogTerm.string)
        self.load_movies(True, False)
        var.SearchTermResult = ''

    def load_movies(self, forceLoad=False, forceUpdate=False, selectIndex=0):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
            xbmcgui.Dialog().notification(var.addonname, "Films worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listContainer.size() > 0: return True
        else:
            guifunc.listReset(listContainer)

        #Add items to list container
        guifunc.updateLabelText(self, 1, "Films laden")
        guifunc.updateLabelText(self, 3, "")
        if limovies.list_load_combined(listContainer, forceUpdate) == False:
            guifunc.updateLabelText(self, 1, 'Niet beschikbaar')
            guifunc.updateLabelText(self, 3, "")
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectItem(listContainer, 0)
            return False

        #Update the status
        self.count_movies(True, selectIndex)

    #Update the status
    def count_movies(self, resetSelect=False, selectIndex=0):
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " films gevonden")
                guifunc.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchTermResult)
            else:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " films")
                guifunc.updateLabelText(self, 3, "")

            if resetSelect == True:
                guifunc.controlFocus(self, listContainer)
                guifunc.listSelectItem(listContainer, selectIndex)
        else:
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.updateLabelText(self, 1, "Geen films gevonden")
                guifunc.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchTermResult)
                guifunc.listSelectItem(listContainer, 1)
            else:
                guifunc.updateLabelText(self, 1, "Geen films")
                guifunc.updateLabelText(self, 3, "")
                guifunc.listSelectItem(listContainer, 0)
