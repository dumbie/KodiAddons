import xbmc
import xbmcgui
import dialog
import download
import func
import path
import lirecorded
import searchdialog
import stream
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
            if listItemAction == 'play_stream':
                stream.play_stream_recorded(listItemSelected, False)
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
                listcontainer = self.getControl(1001)
                self.setFocus(listcontainer)
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
            listcontainer = self.getControl(1000)
            listItemSelected = listcontainer.getSelectedItem()
            ProgramRecordEventId = listItemSelected.getProperty("ProgramRecordEventId")
            ProgramStartDeltaTime = listItemSelected.getProperty("ProgramStartDeltaTime")
            recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramStartDeltaTime)
            if recordRemove == True:
                #Remove item from the list
                removeListItemId = listcontainer.getSelectedPosition()
                listcontainer.removeItem(removeListItemId)
                xbmc.sleep(100)
                listcontainer.selectItem(removeListItemId)
                xbmc.sleep(100)

                #Update the status
                self.count_program(False)
        elif dialogResult == 'Programma zoeken':
            listcontainer = self.getControl(1000)
            listItemSelected = listcontainer.getSelectedItem()
            ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

            #Set search filter term
            var.SearchFilterTerm = func.search_filter_string(ProgramNameRaw)
            self.load_program(True, False)
            var.SearchFilterTerm = ''

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zoek opname')
        listitem.setProperty('Action', 'search_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Vernieuwen")
        listitem.setProperty('Action', 'refresh_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('SearchHistorySearch.js', 'Zoek opname')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_program(True, False)
        var.SearchFilterTerm = ''

    def load_program(self, forceLoad=False, forceUpdate=False, selectIndex=0):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/recorddone.png')
            xbmcgui.Dialog().notification(var.addonname, 'Opnames worden vernieuwd.', notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0: return True
        else:
            listcontainer.reset()

        #Download the programs
        func.updateLabelText(self, 1, "Opnames downloaden")
        downloadResultProfile = download.download_recording_profile(forceUpdate)
        downloadResultEvent = download.download_recording_event(forceUpdate)
        if downloadResultProfile == False and downloadResultEvent == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        func.updateLabelText(self, 1, "Opnames laden")

        #Add items to sort list
        listcontainersort = []
        lirecorded.list_load(listcontainersort)

        #Sort and add items to container
        listcontainersort.sort(key=lambda x: int(x.getProperty('ProgramStartTime')), reverse=True)
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_program(True, selectIndex)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_events()
            var.guiMain.count_recording_events()

    #Update the status
    def count_program(self, resetSelect=False, selectIndex=0):
        func.updateLabelText(self, 4, var.RecordingSpaceString)
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " opnames gevonden")
                func.updateLabelText(self, 3, "[COLOR gray]Zoekresultaten voor[/COLOR] " + var.SearchFilterTerm)
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " opnames")
                func.updateLabelText(self, 3, '')

            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(selectIndex)
                xbmc.sleep(100)
        else:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, 'Geen opnames gevonden')
                func.updateLabelText(self, 3, "[COLOR gray]Geen zoekresultaten voor[/COLOR] " + var.SearchFilterTerm)
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen opnames')
                func.updateLabelText(self, 3, 'Geen opnames beschikbaar.')
                listcontainer.selectItem(0)
            xbmc.sleep(100)
