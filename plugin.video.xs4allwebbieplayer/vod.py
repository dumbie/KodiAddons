import xbmc
import xbmcgui
import dialog
import download
import epg
import func
import livod
import path
import searchdialog
import streamplay
import var

def switch_to_page():
    if var.guiVod == None:
        var.guiVod = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiVod.show()

def close_the_page():
    if var.guiVod != None:
        #Save select index
        var.guiVod.save_select_index()

        #Close the shown window
        var.guiVod.close()
        var.guiVod = None

def source_plugin_list():
    downloadResult = download.download_vod_day(var.VodDayLoadDateTime)
    #if downloadResult == False:
    livod.list_load(None)

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        func.updateLabelText(self, 2, "Programma Gemist")
        self.buttons_add_navigation()
        self.load_program(False, False, True, var.VodSelectIndex)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'play_stream_program':
                streamplay.play_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'set_load_day':
                self.dialog_set_day()
            elif listItemAction == 'refresh_program':
                self.load_program(True, True, False)
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
        elif actionId == var.ACTION_PLAYER_PLAY:
            self.dialog_set_day()
        elif actionId == var.ACTION_PLAYER_FORWARD:
            self.dialog_set_day()
        elif actionId == var.ACTION_PLAYER_REWIND:
            self.dialog_set_day()
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_program()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusItem:
            self.open_context_menu()

    def save_select_index(self):
        listContainer = self.getControl(1000)
        var.VodSelectIndex = listContainer.getSelectedPosition()

    def dialog_set_day(self):
        #Set dates to array
        dialogAnswers = []

        for x in range(var.VodDayOffsetPast + var.VodDayOffsetFuture):
            dayString = func.day_string_from_day_offset(x - var.VodDayOffsetPast)
            dialogAnswers.append(dayString)

        dialogHeader = 'Selecteer dag'
        dialogSummary = 'Selecteer de gewenste programma gemist dag.'
        dialogFooter = ''

        #Get day selection index
        selectIndex = var.VodDayOffsetPast + -func.day_offset_from_datetime(var.VodDayLoadDateTime)

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers, selectIndex)
        if dialogResult == 'DialogCancel':
            return

        #Calculate selected day offset
        selectedIndex = (dialogAnswers.index(dialogResult) - var.VodDayOffsetPast)

        #Update selected day loading time
        var.VodDayLoadDateTime = func.datetime_from_day_offset(selectedIndex)

        #Load day programs
        self.load_program(True, True)

    def open_context_menu(self):
        dialogAnswers = ['Programma zoeken in uitzendingen', 'Programma in de TV Gids tonen']
        dialogHeader = 'Programma Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma zoeken in uitzendingen':
            listContainer = self.getControl(1000)
            listItemSelected = listContainer.getSelectedItem()
            ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

            #Set search filter term
            var.SearchChannelTerm = func.search_filter_string(ProgramNameRaw)
            self.load_program(True, False)
            var.SearchChannelTerm = ''
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

        listItem = xbmcgui.ListItem('Selecteer dag')
        listItem.setProperty('Action', 'set_load_day')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/calendar.png'),'icon': path.resources('resources/skins/default/media/common/calendar.png')})
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

    def load_program(self, forceLoad=False, forceUpdate=False, silentUpdate=True, selectIndex=0):
        if forceUpdate == True and silentUpdate == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
            xbmcgui.Dialog().notification(var.addonname, "Programma's worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listContainer.size() > 0: return True
        else:
            listContainer.reset()

        #Download the programs
        func.updateLabelText(self, 1, "Programma's downloaden")
        func.updateLabelText(self, 3, "")
        downloadResult = download.download_vod_day(var.VodDayLoadDateTime, forceUpdate)
        if downloadResult == False:
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
        livod.list_load(listContainerSort)

        #Sort and add items to container
        listContainer.addItems(listContainerSort)

        #Update the status
        self.count_program(True, selectIndex)

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        #Set the day string
        loadDayString = func.day_string_from_datetime(var.VodDayLoadDateTime)

        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, str(listContainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]op[/COLOR] " + loadDayString)
            else:
                func.updateLabelText(self, 1, str(listContainer.size()) + " programma's")
                func.updateLabelText(self, 3, "[COLOR gray]Beschikbare programma's voor[/COLOR] " + loadDayString)

            if resetSelect == True:
                self.setFocus(listContainer)
                xbmc.sleep(100)
                listContainer.selectItem(selectIndex)
                xbmc.sleep(100)
        else:
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchChannelTerm + " [COLOR gray]op[/COLOR] " + loadDayString)
                listContainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 3, "[COLOR gray]Geen programma's beschikbaar voor[/COLOR] " + loadDayString)
                listContainer.selectItem(0)
            xbmc.sleep(100)
