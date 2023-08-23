import xbmc
import xbmcgui
import dialog
import download
import epg
import files
import func
import metadatainfo
import path
import stream
import var

def switch_to_page():
    if var.guiKids == None:
        var.guiKids = Gui('series.xml', var.addonpath, 'default', '720p')
        var.guiKids.show()

def close_the_page():
    if var.guiKids != None:
        #Check kids page lock
        if page_lock_check() == False:
            notificationIcon = path.resources('resources/skins/default/media/common/kidstongue.png')
            xbmcgui.Dialog().notification(var.addonname, "Helaas pindakaas!", notificationIcon, 2500, False)
            return False

        #Close the shown window
        var.guiKids.close()
        var.guiKids = None
        return True

def page_lock_check():
    if var.addon.getSetting('KidsPageLock') == 'true':
        #Keyboard enter kids pincode
        keyboard = xbmc.Keyboard('default', 'heading')
        keyboard.setHeading('Kids pincode')
        keyboard.setDefault('')
        keyboard.setHiddenInput(True)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            return str(var.addon.getSetting('KidsPincode')) == keyboard.getText()
        return False
    return True

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        func.updateLabelText(self, 3, "Kids")
        self.update_kids_background()
        self.buttons_add_navigation()
        self.load_program(False, False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'load_episodes_vod':
                self.load_episodes_vod(listItemSelected, True)
            elif listItemAction == 'load_episodes_week':
                self.load_episodes_week(listItemSelected, True)
            elif listItemAction == 'play_episode_week':
                stream.play_stream_program(listItemSelected, False)
        elif clickId == 1001:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'go_back':
                close_the_page()
            elif listItemAction == 'search_program':
                self.search_program()
            elif listItemAction == 'refresh_program':
                self.load_program(True, True)
        elif clickId == 1002:
            listItemSelected = clickedControl.getSelectedItem()
            listItemAction = listItemSelected.getProperty('Action')
            if listItemAction == 'play_episode_vod':
                stream.play_stream_vod(listItemSelected, False)
            elif listItemAction == 'play_episode_week':
                stream.play_stream_program(listItemSelected, False)
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
        focusEpisodesList = xbmc.getCondVisibility('Control.HasFocus(1002)')
        focusEpisodesScroll = xbmc.getCondVisibility('Control.HasFocus(2002)')
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            if focusEpisodesList == False and focusEpisodesScroll == False:
                close_the_page()
            else:
                listcontainer = self.getControl(1000)
                self.setFocus(listcontainer)
                xbmc.sleep(100)
        elif actionId == var.ACTION_NEXT_ITEM:
            xbmc.executebuiltin('Action(PageDown)')
        elif actionId == var.ACTION_PREV_ITEM:
            xbmc.executebuiltin('Action(PageUp)')
        elif actionId == var.ACTION_SEARCH_FUNCTION:
            self.search_program()
        elif (actionId == var.ACTION_CONTEXT_MENU or actionId == var.ACTION_DELETE_ITEM) and focusEpisodesList:
            self.open_context_menu()

    def open_context_menu(self):
        listcontainer = self.getControl(1002)
        listItemSelected = listcontainer.getSelectedItem()
        programWeek = listItemSelected.getProperty("ProgramWeek")
        if programWeek == 'true':
            dialogAnswers = ['Aflevering in de TV Gids tonen']
            dialogHeader = 'Aflevering Menu'
            dialogSummary = 'Wat wilt u doen met de geselecteerde aflevering?'
            dialogFooter = ''

            dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
            if dialogResult == 'Aflevering in de TV Gids tonen':
                var.EpgNavigateProgramId = listItemSelected.getProperty("ProgramId")
                var.EpgCurrentChannelId = listItemSelected.getProperty("ChannelId")
                var.EpgCurrentLoadDateTime = func.datetime_from_string(listItemSelected.getProperty("ProgramTimeStartDateTime"), '%Y-%m-%d %H:%M:%S')
                if close_the_page() == True:
                    xbmc.sleep(100)
                    epg.switch_to_page()

    def update_kids_background(self):
        if files.existFile(path.addonstorage("background.png")) == False:
            func.updateImage(self, 8000, 'common/background_addon_kids.png')

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

        listitem = xbmcgui.ListItem("Vernieuwen")
        listitem.setProperty('Action', 'refresh_program')
        listitem.setArt({'thumb': path.resources('resources/skins/default/media/common/refresh.png'), 'icon': path.resources('resources/skins/default/media/common/refresh.png')})
        listcontainer.addItem(listitem)

    def search_program(self):
        try:
            keyboard = xbmc.Keyboard('default', 'heading')
            keyboard.setHeading('Zoek programma')
            keyboard.setDefault('')
            keyboard.setHiddenInput(False)
            keyboard.doModal()
            if keyboard.isConfirmed() == True:
                var.SearchFilterTerm = func.search_filter_string(keyboard.getText())
                self.load_program(True, False)
        except:
            pass
        var.SearchFilterTerm = ''

    def load_episodes_vod(self, listItem, selectList=False):
        #Get the selected parentid
        selectedParentId = listItem.getProperty('ProgramId')
        selectedSeriesName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listcontainer = self.getControl(1002)
        listcontainer.reset()

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen downloaden')

        #Download the series episodes
        seasonDownloaded = download.download_series_season(selectedParentId)
        if seasonDownloaded == None:
            func.updateLabelText(self, 2, 'Afleveringen niet beschikbaar')
            return False

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen laden')

        #Process all the episodes
        for program in seasonDownloaded["resultObj"]["containers"]:
            try:
                #Load program basics
                TechnicalPackageIds = metadatainfo.technicalPackageIds_from_json_metadata(program)

                #Check if content is pay to play
                if metadatainfo.program_check_paytoplay(TechnicalPackageIds): continue

                #Load program details
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
                ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program)
                ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
                ProgramAvailability = metadatainfo.vod_ondemand_available_time(program)

                #Combine program details
                stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisode, ProgramDuration ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'
                ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
                ProgramTitle = ProgramName + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

                #Add vod program
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', 'play_episode_vod')
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramName", ProgramName)
                listitem.setProperty('ProgramDetails', ProgramDetails)
                listitem.setProperty("ProgramAvailability", ProgramAvailability)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': selectedSeriesName, 'Plot': ProgramDescription})
                listitem.setArt({'thumb': path.icon_vod(selectedPictureUrl), 'icon': path.icon_vod(selectedPictureUrl)})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listcontainer.size()) + ' afleveringen)')

        #Select the list container
        if selectList == True and listcontainer.size() > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)

    def load_episodes_week(self, listItem, selectList=False):
        #Get the selected parentid
        selectedSeriesName = listItem.getProperty('ProgramName')
        selectedPictureUrl = listItem.getProperty('PictureUrl')

        #Get and check the list container
        listcontainer = self.getControl(1002)
        listcontainer.reset()
        listcontainersort = []

        #Update the episodes status
        func.updateLabelText(self, 2, 'Afleveringen laden')

        #Process all the episodes
        for program in var.KidsSearchDataJson["resultObj"]["containers"]:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program, True)

                #Check if program matches serie
                checkSerie1 = ProgramName.lower()
                checkSerie2 = selectedSeriesName.lower()
                if checkSerie1 != checkSerie2: continue

                #Load program details
                ChannelId = metadatainfo.channelId_from_json_metadata(program)
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
                ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
                ProgramSeasonInt = metadatainfo.programseason_from_json_metadata(program, False)
                ProgramEpisodeInt = metadatainfo.episodenumber_from_json_metadata(program, False)
                EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, False, ProgramName)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
                ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program)
                ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
                ProgramAvailability = metadatainfo.vod_week_available_time(program)

                #Combine program details
                stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisode, ProgramDuration ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'
                ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
                ProgramTitle = EpisodeTitle + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

                #Add vod program
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', 'play_episode_week')
                listitem.setProperty('ChannelId', ChannelId)
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramTimeStartDateTime", str(ProgramTimeStartDateTime))
                listitem.setProperty("ProgramName", EpisodeTitle)
                listitem.setProperty("ProgramSeasonInt", ProgramSeasonInt)
                listitem.setProperty("ProgramEpisodeInt", ProgramEpisodeInt)
                listitem.setProperty("ProgramWeek", 'true')
                listitem.setProperty('ProgramDetails', ProgramDetails)
                listitem.setProperty("ProgramAvailability", ProgramAvailability)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': selectedSeriesName, 'Plot': ProgramDescription})
                listitem.setArt({'thumb': path.icon_epg(selectedPictureUrl), 'icon': path.icon_epg(selectedPictureUrl)})
                listcontainersort.append(listitem)
            except:
                continue

        #Sort and add episodes
        listcontainersort.sort(key=lambda x: (int(x.getProperty('ProgramSeasonInt')), int(x.getProperty('ProgramEpisodeInt'))))
        listcontainer.addItems(listcontainersort)

        #Update the episodes status
        func.updateLabelText(self, 2, selectedSeriesName + ' (' + str(listcontainer.size()) + ' afleveringen)')

        #Select the list container
        if selectList == True and listcontainer.size() > 0:
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)

    def load_program(self, forceLoad=False, forceUpdate=False):
        if forceUpdate == True:
            notificationIcon = path.resources('resources/skins/default/media/common/kids.png')
            xbmcgui.Dialog().notification(var.addonname, "Programma's worden vernieuwd.", notificationIcon, 2500, False)

        #Get and check the list container
        listcontainer = self.getControl(1000)
        if forceLoad == False and forceUpdate == False:
            if listcontainer.size() > 0: return True
        else:
            listcontainer.reset()

        #Download the programs
        func.updateLabelText(self, 1, "Programma's downloaden")
        downloadResult = download.download_vod_series_kids(forceUpdate)
        downloadResultWeek = download.download_search_kids(forceUpdate)
        if downloadResult == False or downloadResultWeek == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Add programs to the list
        func.updateLabelText(self, 1, "Programma's laden")
        listcontainersort = []
        self.add_program_week(listcontainersort)
        self.add_program_vod(listcontainersort)
        listcontainersort.sort(key=lambda x: x.getProperty('ProgramName'))
        listcontainer.addItems(listcontainersort)

        #Update the status
        self.count_program(True)

        #Load selected episodes
        listItemSelected = listcontainer.getSelectedItem()
        listItemAction = listItemSelected.getProperty('Action')
        if listItemAction == 'load_episodes_vod':
            self.load_episodes_vod(listItemSelected, False)
        elif listItemAction == 'load_episodes_week':
            self.load_episodes_week(listItemSelected, False)

    def add_program_vod(self, listcontainersort):
        for program in var.ChannelsDataJsonSeriesKids['resultObj']['containers']:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch = func.search_filter_string(ProgramName)
                    searchResultFound = var.SearchFilterTerm in searchMatch
                    if searchResultFound == False: continue

                #Load program details
                PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(program)
                ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)

                #Combine program details
                stringJoin = [ ProgramYear, ProgramStarRating, ProgramAgeRating ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'
                ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'

                #Add vod program
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', 'load_episodes_vod')
                listitem.setProperty('PictureUrl', PictureUrl)
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramName", ProgramName)
                listitem.setProperty('ProgramDetails', ProgramDetails)
                listitem.setInfo('video', {'Genre': 'Series', 'Plot': ProgramDetails})
                iconProgramType = "common/series.png"
                iconStreamType = "common/vod.png"
                iconProgram = path.icon_vod(PictureUrl)
                listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType})
                listcontainersort.append(listitem)
            except:
                continue

    def add_program_week(self, listcontainersort):
        for program in var.KidsSearchDataJson['resultObj']['containers']:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program, True)

                #Check if serie is already added
                if func.search_programname_listarray(listcontainersort, ProgramName) != None: continue

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch = func.search_filter_string(ProgramName)
                    searchResultFound = var.SearchFilterTerm in searchMatch
                    if searchResultFound == False: continue

                #Check if program is serie or movie
                ContentSubtype = metadatainfo.contentSubtype_from_json_metadata(program)
                if ContentSubtype == "VOD":
                    ProgramAction = 'play_episode_week'
                    iconProgramType = "common/movies.png"
                    ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program, False)
                    ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
                    ProgramAvailability = metadatainfo.vod_week_available_time(program)
                else:
                    ProgramAction = 'load_episodes_week'
                    iconProgramType = "common/series.png"
                    ProgramDuration = ""
                    ProgramDescription = ""
                    ProgramAvailability = ""

                #Load program details
                ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
                PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
                SeriesId = metadatainfo.seriesId_from_json_metadata(program)
                ProgramId = metadatainfo.contentId_from_json_metadata(program)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(program)
                ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)

                #Combine program details
                stringJoin = [ ProgramYear, ProgramStarRating, ProgramAgeRating, ProgramDuration ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'
                ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'
                ProgramTitle = ProgramName + " [COLOR gray]" + ProgramDetails + "[/COLOR]"

                #Add week program
                listitem = xbmcgui.ListItem()
                listitem.setProperty('Action', ProgramAction)
                listitem.setProperty('PictureUrl', PictureUrl)
                listitem.setProperty('SeriesId', SeriesId)
                listitem.setProperty('ProgramId', ProgramId)
                listitem.setProperty("ProgramName", ProgramName)
                listitem.setProperty("ProgramWeek", 'true')
                listitem.setProperty('ProgramDetails', ProgramDetails)
                listitem.setProperty("ProgramAvailability", ProgramAvailability)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setInfo('video', {'Title': ProgramTitle, 'Genre': 'Kids', 'Plot': ProgramDescription})
                iconStreamType = "common/calendarweek.png"
                iconProgram = path.icon_epg(PictureUrl)
                iconChannel = path.icon_television(ExternalId)
                listitem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconProgramType, 'image3': iconChannel})
                listcontainersort.append(listitem)
            except:
                continue

    #Update the status
    def count_program(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            func.updateVisibility(self, 2, True)
            func.updateVisibility(self, 3002, True)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's gevonden")
                func.updateLabelText(self, 4, "Zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR]")
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " programma's")
                func.updateLabelText(self, 4, "")

            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateVisibility(self, 2, False)
            func.updateVisibility(self, 3002, False)
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, "Geen programma's gevonden")
                func.updateLabelText(self, 4, "Geen zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR]")
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, "Geen programma's")
                func.updateLabelText(self, 4, "")
                listcontainer.selectItem(0)
            xbmc.sleep(100)
