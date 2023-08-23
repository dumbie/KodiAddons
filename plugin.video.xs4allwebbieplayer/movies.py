import xbmc
import xbmcgui
import dialog
import download
import epg
import func
import metadatainfo
import path
import stream
import var

def switch_to_page():
    if var.guiMovies == None:
        var.guiMovies = Gui('movies.xml', var.addonpath, 'default', '720p')
        var.guiMovies.show()

def close_the_page():
    if var.guiMovies != None:
        #Close the shown window
        var.guiMovies.close()
        var.guiMovies = None

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        self.buttons_add_navigation()
        self.load_movies(False, False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'play_stream_vod':
                stream.play_stream_vod(listItemSelected, False)
            elif listItemAction == 'play_stream_week':
                stream.play_stream_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'refresh_programs':
                self.load_movies(True, True)
            elif listItemAction == 'search_movie':
                self.search_movie()
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
            self.search_movie()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusItem:
            self.open_context_menu()

    def open_context_menu(self):
        listcontainer = self.getControl(1000)
        listItemSelected = listcontainer.getSelectedItem()
        programWeek = listItemSelected.getProperty("ProgramWeek")
        if programWeek == 'true':
            dialogAnswers = ['Film in de TV Gids tonen']
            dialogHeader = 'Film Menu'
            dialogSummary = 'Wat wilt u doen met de geselecteerde film?'
            dialogFooter = ''

            dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
            if dialogResult == 'Film in de TV Gids tonen':
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

        listitem = xbmcgui.ListItem("Zoek naar film")
        listitem.setProperty('Action', 'search_movie')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/search.png'), 'icon': path.resources('resources/skins/default/media/common/search.png')})
        listcontainer.addItem(listitem)

        listitem = xbmcgui.ListItem("Vernieuwen")
        listitem.setProperty('Action', 'refresh_programs')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def search_movie(self):
        try:
            keyboard = xbmc.Keyboard('default', 'heading')
            keyboard.setHeading('Zoek naar film')
            keyboard.setDefault('')
            keyboard.setHiddenInput(False)
            keyboard.doModal()
            if keyboard.isConfirmed() == True:
                var.SearchFilterTerm = func.search_filter_string(keyboard.getText())
                self.load_movies(True, False)
        except:
            pass
        var.SearchFilterTerm = ''

    def load_movies(self, forceLoad=False, forceUpdate=False):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/movies.png')
            xbmcgui.Dialog().notification(var.addonname, "Films worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0: return True
        else:
            listcontainer.reset()

        #Download the movies
        func.updateLabelText(self, 1, "Films downloaden")
        downloadResult = download.download_vod_movies(forceUpdate)
        downloadResultWeek = download.download_search_movies(forceUpdate)
        if downloadResult == False or downloadResultWeek == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Add movies to the list
        func.updateLabelText(self, 1, "Films laden")
        listcontainersort = []
        self.add_movies_week(listcontainersort)
        self.add_movies_vod(listcontainersort)
        listcontainersort.sort(key=lambda x: x.getProperty('ProgramName'))
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_movies(True)

    def add_movies_vod(self, listcontainersort):
        for program in var.ChannelsDataJsonMovies['resultObj']['containers']:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)
                TechnicalPackageIds = metadatainfo.technicalPackageIds_from_json_metadata(program)

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch = func.search_filter_string(ProgramName)
                    searchResultFound = var.SearchFilterTerm in searchMatch
                    if searchResultFound == False: continue

                #Check if content is pay to play
                if metadatainfo.program_check_paytoplay(TechnicalPackageIds): continue

                #Load program details
                PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(program)
                ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)
                ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program)
                ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
                ProgramAvailability = metadatainfo.vod_ondemand_available_time(program)

                #Combine program details
                stringJoin = [ ProgramYear, ProgramSeason, ProgramStarRating, ProgramAgeRating, ProgramDuration ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'
                ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
                ProgramTitle = ProgramName + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

                #Add vod program
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', 'play_stream_vod')
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramName", ProgramName)
                listitem.setProperty("ProgramDetails", ProgramDetails)
                listitem.setProperty("ProgramAvailability", ProgramAvailability)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Films', 'Plot': ProgramDescription})
                iconStreamType = "common/vod.png"
                iconProgram = path.icon_vod(PictureUrl)
                listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType})
                listcontainersort.append(listitem)
            except:
                continue

    def add_movies_week(self, listcontainersort):
        for program in var.MovieSearchDataJson['resultObj']['containers']:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program, True)

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch = func.search_filter_string(ProgramName)
                    searchResultFound = var.SearchFilterTerm in searchMatch
                    if searchResultFound == False: continue

                #Load program details
                ChannelId = metadatainfo.channelId_from_json_metadata(program)
                ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
                PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
                ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(program)
                ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)
                ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program)
                ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
                ProgramAvailability = metadatainfo.vod_week_available_time(program)

                #Combine program details
                stringJoin = [ ProgramYear, ProgramSeason, ProgramStarRating, ProgramAgeRating, ProgramDuration ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'
                ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
                ProgramTitle = ProgramName + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

                #Add week program
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', 'play_stream_week')
                listitem.setProperty('ChannelId', ChannelId)
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
                listitem.setProperty("ProgramName", ProgramName)
                listitem.setProperty("ProgramWeek", 'true')
                listitem.setProperty("ProgramDetails", ProgramDetails)
                listitem.setProperty("ProgramAvailability", ProgramAvailability)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Films', 'Plot': ProgramDescription})
                iconStreamType = "common/calendarweek.png"
                iconProgram = path.icon_epg(PictureUrl)
                iconChannel = path.icon_television(ExternalId)
                listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconChannel})
                listcontainersort.append(listitem)
            except:
                continue

    #Update the status
    def count_movies(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " gevonden films")
                func.updateLabelText(self, 3, "Zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR]")
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " films")
                func.updateLabelText(self, 3, "")

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
                func.updateLabelText(self, 1, "Geen films gevonden")
                func.updateLabelText(self, 3, "Geen zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR]")
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, "Geen films")
                func.updateLabelText(self, 3, "")
                listcontainer.selectItem(0)
            xbmc.sleep(100)
