from datetime import datetime, timedelta
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
    if var.guiVod == None:
        var.guiVod = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiVod.show()

def close_the_page():
    if var.guiVod != None:
        #Close the shown window
        var.guiVod.close()
        var.guiVod = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        func.updateLabelText(self, 2, "Programma Gemist")
        self.buttons_add_navigation()
        self.load_program(False, False)

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
            elif listItemAction == 'set_load_day':
                self.dialog_set_day()
            elif listItemAction == 'refresh_program':
                self.load_program(True, True, False)
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

    def dialog_set_day(self):
        #Set dates to array
        dialogAnswers = []

        for x in range(var.VodDaysOffsetPast + var.VodDaysOffsetFuture):
            dayString = func.day_string_from_day_offset(x - var.VodDaysOffsetPast)
            dialogAnswers.append(dayString)

        dialogHeader = 'Selecteer dag'
        dialogSummary = 'Selecteer de gewenste programma gemist dag.'
        dialogFooter = ''

        #Get day selection index
        selectIndex = var.VodDaysOffsetPast + -func.day_offset_from_datetime(var.VodCurrentLoadDateTime)

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers, selectIndex)
        if dialogResult == 'DialogCancel':
            return

        #Calculate selected day offset
        selectedIndex = (dialogAnswers.index(dialogResult) - var.VodDaysOffsetPast)

        #Update selected day loading time
        var.VodCurrentLoadDateTime = func.datetime_from_day_offset(selectedIndex)

        #Load day programs
        self.load_program(True, True)

    def open_context_menu(self):
        dialogAnswers = ['Programma zoeken in uitzendingen', 'Programma in de TV Gids tonen']
        dialogHeader = 'Programma Menu'
        dialogSummary = 'Wat wilt u doen met de geselecteerde programma?'
        dialogFooter = ''

        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Programma zoeken in uitzendingen':
            listcontainer = self.getControl(1000)
            listItemSelected = listcontainer.getSelectedItem()
            ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")

            #Set search filter term
            var.SearchFilterTerm = func.search_filter_string(ProgramNameRaw)
            self.load_program(True, False)
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

        listitem = xbmcgui.ListItem('Selecteer dag')
        listitem.setProperty('Action', 'set_load_day')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/calendar.png'),'icon': path.resources('resources/skins/default/media/common/calendar.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Vernieuwen")
        listitem.setProperty('Action', 'refresh_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def search_program(self):
        #Open the search dialog
        searchDialogTerm = searchdialog.search_dialog('Zoek programma')

        #Check the search term
        if searchDialogTerm.cancelled == True:
            return

        #Set search filter term
        var.SearchFilterTerm = func.search_filter_string(searchDialogTerm.string)
        self.load_program(True, False)
        var.SearchFilterTerm = ''

    def load_program(self, forceLoad=False, forceUpdate=False, silentUpdate=True):
        if forceUpdate == True and silentUpdate == False:
            notificationIcon = path.resources('resources/skins/default/media/common/vod.png')
            xbmcgui.Dialog().notification(var.addonname, "Programma's worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0: return True
        else:
            listcontainer.reset()

        #Download the programs
        func.updateLabelText(self, 1, "Programma's downloaden")
        func.updateLabelText(self, 3, "")
        downloadResult = download.download_vod_day(var.VodCurrentLoadDateTime, forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Add programs to the list
        func.updateLabelText(self, 1, "Programma's laden")
        for program in var.VodCurrentDataJson['resultObj']['containers']:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)
                ProgramNameRaw = ProgramName
                EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True, ProgramNameRaw)
                ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(program)

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch1 = func.search_filter_string(ProgramName)
                    searchMatch2 = func.search_filter_string(EpisodeTitle)
                    searchResultFound = var.SearchFilterTerm in searchMatch1 or var.SearchFilterTerm in searchMatch2
                    if searchResultFound == False: continue

                #Check if program has finished airing and processing
                if datetime.now() < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue

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

                #Combine program details
                stringJoin = [ EpisodeTitle, ProgramYear, ProgramSeason, ProgramEpisode, ProgramAgeRating ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'

                #Update program name string
                ProgramName = ProgramNameRaw + ' [COLOR gray]' + ProgramDetails + '[/COLOR]'
                ProgramNameDesc = ProgramNameRaw + '\n[COLOR gray]' + ProgramDetails + '[/COLOR]'

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
                listitem.setInfo('video', {'Genre': 'Programma Gemist', 'Plot': ProgramDescription})
                listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the status
        self.count_program(True)

    #Update the status
    def count_program(self, resetSelect=False):
        #Set the day string
        loadDayString = func.day_string_from_datetime(var.VodCurrentLoadDateTime)

        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 3, "Zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR] op [COLOR gray]" + loadDayString + "[/COLOR]")
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's")
                func.updateLabelText(self, 3, "Beschikbare programma's voor [COLOR gray]" + loadDayString + "[/COLOR]")

            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 3, "Geen zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR] op [COLOR gray]" + loadDayString + "[/COLOR]")
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 3, "Geen programma's beschikbaar voor [COLOR gray]" + loadDayString + "[/COLOR]")
                listcontainer.selectItem(0)
            xbmc.sleep(100)
