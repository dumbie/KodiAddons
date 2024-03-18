import xbmc
import xbmcgui
import dialog
import dlrecordingrequest
import func
import guifunc
import lifunc
import lirecorded
import path
import player
import searchdialog
import streamplay
import var

def switch_to_page():
    if var.guiRecorded == None:
        var.guiRecorded = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiRecorded.setProperty('WebbiePlayerPage', 'Open')
        var.guiRecorded.show()

def close_the_page():
    if var.guiRecorded != None:
        #Save select index
        var.guiRecorded.save_select_index()

        #Close the shown window
        var.guiRecorded.close()
        var.guiRecorded = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        guifunc.updateLabelText(self, 2, "Opnames")
        self.buttons_add_navigation()
        self.load_program(False, var.RecordedSelectIdentifier)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'play_stream_recorded':
                streamplay.play_recorded(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('ItemAction')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
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
        try:
            listContainer = self.getControl(1000)
            listItemSelected = listContainer.getSelectedItem()
            var.RecordedSelectIdentifier = listItemSelected.getProperty("ProgramRecordEventId")
        except:
            pass

    def open_context_menu(self):
        dialogAnswers = ['Opname verwijderen', 'Programma zoeken in opnames']
        dialogHeader = 'Opname Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde opname?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Opname verwijderen':
            listContainer = self.getControl(1000)
            listItemSelected = listContainer.getSelectedItem()
            ProgramRecordEventId = listItemSelected.getProperty("ProgramRecordEventId")
            ProgramDeltaTimeStart = listItemSelected.getProperty("ProgramDeltaTimeStart")
            recordRemove = dlrecordingrequest.event_remove(ProgramRecordEventId, ProgramDeltaTimeStart)
            if recordRemove == True:
                #Remove item from the list
                removeListItemIndex = listContainer.getSelectedPosition()
                guifunc.listRemoveItem(listContainer, removeListItemIndex)
                guifunc.listSelectIndex(listContainer, removeListItemIndex)

                #Update the status
                self.count_program(False)
        elif dialogResult == 'Programma zoeken in opnames':
            self.search_program_result()

    def buttons_add_navigation(self):
        listContainer = self.getControl(1001)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga een stap terug')
        listItem.setProperty('ItemAction', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek opname')
        listItem.setProperty('ItemAction', 'search_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

    def search_program_result(self):
        listContainer = self.getControl(1000)
        listItemSelected = listContainer.getSelectedItem()
        ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

        #Set search filter term
        var.SearchTermResult = func.search_filter_string(ProgramNameRaw)
        self.load_program(True)
        var.SearchTermResult = ''

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek opname')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchTermResult = func.search_filter_string(searchDialogTerm.string)
        self.load_program(True)
        var.SearchTermResult = ''

    def load_program(self, forceLoad=False, selectIdentifier=""):
        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False:
            if listContainer.size() > 0: return True
        else:
            guifunc.listReset(listContainer)

        #Add items to list container
        guifunc.updateLabelText(self, 1, "Opnames laden")
        guifunc.updateLabelText(self, 3, "")
        if lirecorded.list_load_combined(listContainer) == False:
            guifunc.updateLabelText(self, 1, 'Niet beschikbaar')
            guifunc.updateLabelText(self, 3, "")
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            guifunc.listSelectIndex(listContainer, 0)
            return False

        #Update the status
        self.count_program(True, selectIdentifier)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

    #Update the status
    def count_program(self, resetSelect=False, selectIdentifier=""):
        guifunc.updateLabelText(self, 4, var.RecordingAvailableSpace())
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " opnames gevonden")
                guifunc.updateLabelText(self, 3, "[COLOR FF888888]Zoekresultaten voor[/COLOR] " + var.SearchTermResult)
            else:
                guifunc.updateLabelText(self, 1, str(listContainer.size()) + " opnames")
                guifunc.updateLabelText(self, 3, "")

            if resetSelect == True:
                guifunc.controlFocus(self, listContainer)
                listIndex = lifunc.search_listcontainer_property_listindex(listContainer, 'ProgramRecordEventId', selectIdentifier)
                guifunc.listSelectIndex(listContainer, listIndex)
        else:
            listContainer = self.getControl(1001)
            guifunc.controlFocus(self, listContainer)
            if func.string_isnullorempty(var.SearchTermResult) == False:
                guifunc.updateLabelText(self, 1, 'Geen opnames gevonden')
                guifunc.updateLabelText(self, 3, "[COLOR FF888888]Geen zoekresultaten voor[/COLOR] " + var.SearchTermResult)
                guifunc.listSelectIndex(listContainer, 1)
            else:
                guifunc.updateLabelText(self, 1, 'Geen opnames')
                guifunc.updateLabelText(self, 3, 'Geen opnames beschikbaar.')
                guifunc.listSelectIndex(listContainer, 0)
