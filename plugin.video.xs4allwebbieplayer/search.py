import xbmc
import xbmcgui
import dialog
import download
import func
import hybrid
import metadatainfo
import path
import searchhistory
import stream
import var

def switch_to_page():
    if var.guiSearch == None:
        var.guiSearch = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiSearch.show()

def close_the_page():
    if var.guiSearch != None:
        #Close the shown window
        var.guiSearch.close()
        var.guiSearch = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        #Load search history
        searchhistory.search_json_load()

        #Prepare the search page
        func.updateLabelText(self, 2, "Zoeken")
        self.buttons_add_navigation()
        listcontainer = self.getControl(1000)
        if listcontainer.size() == 0:
            if var.SearchDownloadResultJson == []:
                self.search_program()
            else:
                self.search_list(var.SearchDownloadResultJson)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'play_stream':
                stream.play_stream_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'search_history':
                self.search_history()
            elif listItemAction == 'search_result':
                self.search_result()
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

    def open_context_menu(self):
        dialogAnswers = ['Programma zoeken']
        dialogHeader = 'Programma zoeken'
        dialogSummary = 'Wilt u naar de geselecteerde programma zoeken?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma zoeken':
            try:
                listcontainer = self.getControl(1000)
                listItemSelected = listcontainer.getSelectedItem()
                ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")
                var.SearchFilterTerm = func.search_filter_string(ProgramNameRaw)
                self.search_list(var.SearchDownloadResultJson)
            except:
                pass
            var.SearchFilterTerm = ''

    def buttons_add_navigation(self):
        listcontainer = self.getControl(1001)
        if listcontainer.size() > 0: return True

        listitem = xbmcgui.ListItem('Ga een stap terug')
        listitem.setProperty('Action', 'go_back')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/back.png'), 'icon': path.resources('resources/skins/default/media/common/back.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Zoek programma")
        listitem.setProperty('Action', 'search_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem('Zoekgeschiedenis')
        listitem.setProperty('Action', 'search_history')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/searchhistory.png'), 'icon': path.resources('resources/skins/default/media/common/searchhistory.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Zoek in resultaat")
        listitem.setProperty('Action', 'search_result')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/searchresult.png'), 'icon': path.resources('resources/skins/default/media/common/searchresult.png')})
        listcontainer.addItem(listitem)

    def search_result(self):
        #Check if search result is available
        if var.SearchDownloadResultJson == []:
            notificationIcon = path.resources('resources/skins/default/media/common/searchresult.png')
            xbmcgui.Dialog().notification(var.addonname, 'Geen zoekresultaten.', notificationIcon, 2500, False)
            return

        #Keyboard enter filter term
        keyboard = xbmc.Keyboard('default', 'heading')
        keyboard.setHeading('Zoek in resultaat')
        keyboard.setDefault('')
        keyboard.setHiddenInput(False)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            var.SearchFilterTerm = func.search_filter_string(keyboard.getText())
            self.search_list(var.SearchDownloadResultJson)
            var.SearchFilterTerm = ''

    def search_program(self):
        #Keyboard enter search term
        keyboard = xbmc.Keyboard('default', 'heading')
        keyboard.setHeading('Zoek programma')
        keyboard.setDefault('')
        keyboard.setHiddenInput(False)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            searchProgramName = keyboard.getText()
        else:
            func.updateLabelText(self, 1, 'Geen zoek term')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(1)
            xbmc.sleep(100)
            return False

        #Check the search term
        if func.string_isnullorempty(searchProgramName) == True:
            func.updateLabelText(self, 1, 'Leeg zoek term')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(1)
            xbmc.sleep(100)
            return False

        #Add search history to Json
        searchhistory.search_add(searchProgramName)

        #Download the search programs
        func.updateLabelText(self, 1, "Zoek resultaat downloaden")
        downloadResult = download.download_search_program(searchProgramName)
        if downloadResult == None:
            func.updateLabelText(self, 1, 'Zoeken mislukt')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Update the search result
        var.SearchDownloadSearchTerm = searchProgramName
        var.SearchDownloadResultJson = downloadResult

        #List the search results
        func.updateLabelText(self, 1, "Zoek resultaat laden")
        self.search_list(var.SearchDownloadResultJson)

    def search_history(self):
        #Get search term
        searchProgramName = searchhistory.search_dialog()

        #Check search term
        if func.string_isnullorempty(searchProgramName) == True:
            return

        #Add search history to Json
        searchhistory.search_add(searchProgramName)

        #Download the search programs
        func.updateLabelText(self, 1, "Zoek resultaat downloaden")
        downloadResult = download.download_search_program(searchProgramName)
        if downloadResult == None:
            func.updateLabelText(self, 1, 'Zoeken mislukt')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Update the search result
        var.SearchDownloadSearchTerm = searchProgramName
        var.SearchDownloadResultJson = downloadResult

        #List the search results
        func.updateLabelText(self, 1, "Zoek resultaat laden")
        self.search_list(var.SearchDownloadResultJson)

    def search_list(self, downloadResult=None):
        #Get and check the list container
        listcontainer = self.getControl(1000)
        listcontainer.reset()

        #Add programs to the list
        for program in downloadResult['resultObj']['containers']:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)
                ProgramNameRaw = ProgramName
                EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True, ProgramNameRaw)

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch1 = func.search_filter_string(ProgramName)
                    searchMatch2 = func.search_filter_string(EpisodeTitle)
                    searchResultFound = var.SearchFilterTerm in searchMatch1 or var.SearchFilterTerm in searchMatch2
                    if searchResultFound == False: continue

                #Load program details
                ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
                ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)
                ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program, False)
                ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
                ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
                ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
                ProgramTimeStartStringTime = ProgramTimeStartDateTime.strftime('%H:%M')
                ProgramTimeStartStringDate = ProgramTimeStartDateTime.strftime('%a, %d %B %Y')
                ProgramTime = '[COLOR gray]Begon om ' + ProgramTimeStartStringTime + ' op ' + ProgramTimeStartStringDate + ' en duurde ' + ProgramDuration + '[/COLOR]'
                ProgramAvailability = metadatainfo.vod_week_available_time(program)

                #Combine program details
                stringJoin = [ EpisodeTitle, ProgramYear, ProgramSeason, ProgramEpisode, ProgramAgeRating ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'

                #Update program name string
                ProgramName = ProgramNameRaw + ' [COLOR gray]' + ProgramDetails + '[/COLOR]'
                ProgramNameDesc = ProgramNameRaw + '\n[COLOR gray]' + ProgramDetails + '[/COLOR]\n' + ProgramAvailability

                #Add program
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', 'play_stream')
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramName", ProgramName)
                listitem.setProperty("ProgramNameDesc", ProgramNameDesc)
                listitem.setProperty("ProgramNameRaw", ProgramNameRaw)
                listitem.setProperty("ProgramDetails", ProgramTime)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setInfo('video', {'Genre': 'Zoeken', 'Plot': ProgramDescription})
                listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the status
        self.count_program(True)

    #Update the status
    def count_program(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            func.updateLabelText(self, 1, str(listcontainer.size()) + " zoekresultaten")
            if func.string_isnullorempty(var.SearchFilterTerm):
                func.updateLabelText(self, 3, "Zoekresultaten voor [COLOR gray]" + var.SearchDownloadSearchTerm + "[/COLOR]")
            else:
                func.updateLabelText(self, 3, "Zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR] in [COLOR gray]" + var.SearchDownloadSearchTerm + "[/COLOR]")
            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 1, "Geen zoekresultaten")
            if func.string_isnullorempty(var.SearchFilterTerm):
                func.updateLabelText(self, 3, "Geen zoekresultaten voor [COLOR gray]" + var.SearchDownloadSearchTerm + "[/COLOR]")
            else:
                func.updateLabelText(self, 3, "Geen zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR] in [COLOR gray]" + var.SearchDownloadSearchTerm + "[/COLOR]")
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                listcontainer.selectItem(3)
            else:
                listcontainer.selectItem(1)
            xbmc.sleep(100)
