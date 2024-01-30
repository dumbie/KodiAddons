import xbmc
import xbmcgui
import dialog
import download
import func
import lifunc
import metadatainfo
import path
import lirecorded
import searchdialog
import streamplay
import var

def switch_to_page():
    if var.guiRecorded == None:
        var.guiRecorded = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiRecorded.show()

def close_the_page():
    if var.guiRecorded != None:
        #Save select index
        var.guiRecorded.save_select_index()

        #Close the shown window
        var.guiRecorded.close()
        var.guiRecorded = None

def source_plugin_list():
    downloadResultProfile = download.download_recording_profile()
    downloadResultEvent = download.download_recording_event()
    #if downloadResultProfile == False and downloadResultEvent == False:

    #Add items to sort list
    listContainerSort = []
    lirecorded.list_load(listContainerSort)

    #Sort items in list
    listContainerSort.sort(key=lambda x: int(x.getProperty('ProgramStartTime')), reverse=True)

    #Add items to container
    for listItem in listContainerSort:
        ListAction = listItem.getProperty('Action')
        ProgramAssetId = listItem.getProperty('ProgramAssetId')
        ProgramRecordEventId = listItem.getProperty('ProgramRecordEventId')
        lifunc.auto_add_item(listItem, None, dirUrl=ListAction+'='+ProgramAssetId+var.splitchar+ProgramRecordEventId)
    lifunc.auto_end_items()

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        func.updateLabelText(self, 2, "Opnames")
        self.buttons_add_navigation()
        self.load_program(False, False, var.RecordedSelectIndex)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'play_stream_recorded':
                streamplay.play_recorded(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'refresh_program':
                self.load_program(True, True)
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
        var.RecordedSelectIndex = listContainer.getSelectedPosition()

    def open_context_menu(self):
        dialogAnswers = ['Opname verwijderen', 'Programma zoeken']
        dialogHeader = 'Opname verwijderen of programma zoeken'
        dialogSummary = 'Wilt u de geselecteerde opname verwijderen of wilt u alleen naar dit programma zoeken in de opnames?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Opname verwijderen':
            listContainer = self.getControl(1000)
            listItemSelected = listContainer.getSelectedItem()
            ProgramRecordEventId = listItemSelected.getProperty("ProgramRecordEventId")
            ProgramStartDeltaTime = listItemSelected.getProperty("ProgramStartDeltaTime")
            recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramStartDeltaTime)
            if recordRemove == True:
                #Remove item from the list
                removeListItemId = listContainer.getSelectedPosition()
                listContainer.removeItem(removeListItemId)
                xbmc.sleep(100)
                listContainer.selectItem(removeListItemId)
                xbmc.sleep(100)

                #Update the status
                self.count_program(False)
        elif dialogResult == 'Programma zoeken':
            listContainer = self.getControl(1000)
            listItemSelected = listContainer.getSelectedItem()
            ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

            #Set search filter term
            var.SearchChannelTerm = func.search_filter_string(ProgramNameRaw)
            self.load_program(True, False)
            var.SearchChannelTerm = ''

    def buttons_add_navigation(self):
        listContainer = self.getControl(1001)
        if listContainer.size() > 0: return True

        listItem = xbmcgui.ListItem('Ga een stap terug')
        listItem.setProperty('Action', 'go_back')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem('Zoek opname')
        listItem.setProperty('Action', 'search_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listContainer.addItem(listItem)

        listItem = xbmcgui.ListItem("Vernieuwen")
        listItem.setProperty('Action', 'refresh_program')
        listItem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listContainer.addItem(listItem)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek opname')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchChannelTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_program(True, False)
        var.SearchChannelTerm = ''

    def load_program(self, forceLoad=False, forceUpdate=False, selectIndex=0):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opnames worden vernieuwd.', notificationIcon, 2500, False)

        #Get and check the list container
        listContainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listContainer.size() > 0: return True
        else:
            listContainer.reset()

        #Download the programs
        func.updateLabelText(self, 1, "Opnames downloaden")
        downloadResultProfile = download.download_recording_profile(forceUpdate)
        downloadResultEvent = download.download_recording_event(forceUpdate)
        if downloadResultProfile == False and downloadResultEvent == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listContainer = self.getControl(1001)
            self.setFocus(listContainer)
            xbmc.sleep(100)
            listContainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, "Opnames laden")

        #Add items to sort list
        listContainerSort = []
        lirecorded.list_load(listContainerSort)

        #Sort and add items to container
        listContainerSort.sort(key=lambda x: int(x.getProperty('ProgramStartTime')), reverse=True)
        listContainer.addItems(listContainerSort)

        #Update the status
        self.count_program(True, selectIndex)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        func.updateLabelText(self, 4, var.RecordingAvailableSpace())
        listContainer = self.getControl(1000)
        if listContainer.size() > 0:
            if var.SearchChannelTerm != '':
                func.updateLabelText(self, 1, str(listContainer.size()) + " opnames gevonden")
                func.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
            else:
                func.updateLabelText(self, 1, str(listContainer.size()) + " opnames")
                func.updateLabelText(self, 3, '')

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
                func.updateLabelText(self, 1, 'Geen opnames gevonden')
                func.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchChannelTerm)
                listContainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen opnames')
                func.updateLabelText(self, 3, 'Geen opnames beschikbaar.')
                listContainer.selectItem(0)
            xbmc.sleep(100)
