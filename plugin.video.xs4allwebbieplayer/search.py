import xbmc
import xbmcgui
import dialog
import download
import epg
import func
import metadatainfo
import path
import searchdialog
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
        #Prepare the search page
        func.updateLabelText(self, 2, "Zoeken")
        self.buttons_add_navigation()
        listcontainer = self.getControl(1000)
        if listcontainer.size() == 0:
            if var.SearchDownloadResultJson == []:
                func.updateLabelText(self, 1, 'Geen zoek term')
                listcontainer = self.getControl(1001)
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(1)
                xbmc.sleep(100)
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
        dialogAnswers = ['Programma zoeken in resultaat', 'Programma in de TV Gids tonen']
        dialogHeader = 'Programma Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma zoeken in resultaat':
            listcontainer = self.getControl(1000)
            listItemSelected = listcontainer.getSelectedItem()
            ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

            #Set search filter term
            var.SearchFilterTerm = func.search_filter_string(ProgramNameRaw)
            self.search_list(var.SearchDownloadResultJson)
            var.SearchFilterTerm = ''
        elif dialogResult == 'Programma in de TV Gids tonen':
            listcontainer = self.getControl(1000)
            listItemSelected = listcontainer.getSelectedItem()
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

        listitem = xbmcgui.ListItem("Zoek programma")
        listitem.setProperty('Action', 'search_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
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

        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek in resultaat')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        self.search_list(var.SearchDownloadResultJson)
        var.SearchFilterTerm = ''

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek programma')

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
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Update the search result
        var.SearchDownloadSearchTerm = searchDialogTerm.string
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
                EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True)

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch1 = func.search_filter_string(ProgramName)
                    searchMatch2 = func.search_filter_string(EpisodeTitle)
                    searchResultFound = var.SearchFilterTerm in searchMatch1 or var.SearchFilterTerm in searchMatch2
                    if searchResultFound == False: continue

                #Load program details
                ChannelId = metadatainfo.channelId_from_json_metadata(program)
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
                listitem.setProperty('ChannelId', ChannelId)
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
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
