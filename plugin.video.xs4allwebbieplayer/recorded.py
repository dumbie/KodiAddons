import json
from datetime import datetime, timedelta
import xbmc
import xbmcgui
import apilogin
import dialog
import download
import func
import metadatainfo
import path
import stream
import var

def switch_to_page():
    if var.guiRecorded == None:
        var.guiRecorded = Gui('vod.xml', var.addonpath, 'default', '720p')
        var.guiRecorded.show()

def close_the_page():
    if var.guiRecorded != None:
        #Close the shown window
        var.guiRecorded.close()
        var.guiRecorded = None

def count_main_recording():
    #Download the recording programs
    downloadResult = download.download_recording_event(False)
    if downloadResult == False: return '?'

    #Count planned recording
    recordingCount = 0
    for program in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
        try:
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)
            if datetime.now() < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue
            recordingCount += 1
        except:
            continue
    return recordingCount

class Gui(xbmcgui.WindowXML):
    def onInit(self):
        func.updateLabelText(self, 2, "Opnames")
        self.buttons_add_navigation()
        self.load_program(False, False)

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
            try:
                listcontainer = self.getControl(1000)
                listItemSelected = listcontainer.getSelectedItem()
                ProgramNameRaw = listItemSelected.getProperty("ProgramNameRaw")
                var.SearchFilterTerm = func.search_filter_string(ProgramNameRaw)
                self.load_program(True, False)
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

        listitem = xbmcgui.ListItem('Zoek opname')
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
            keyboard.setHeading('Zoek opname')
            keyboard.setDefault('')
            keyboard.setHiddenInput(False)
            keyboard.doModal()
            if keyboard.isConfirmed() == True:
                var.SearchFilterTerm = func.search_filter_string(keyboard.getText())
                self.load_program(True, False)
        except:
            pass
        var.SearchFilterTerm = ''

    def load_program(self, forceLoad=False, forceUpdate=False):
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
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 1, 'Niet beschikbaar')
            listcontainer = self.getControl(1001)
            self.setFocus(listcontainer)
            xbmc.sleep(100)
            listcontainer.selectItem(0)
            xbmc.sleep(100)
            return False

        #Add programs to the list
        func.updateLabelText(self, 1, "Opnames laden")
        for program in var.ChannelsDataJsonRecordingEvent['resultObj']['containers']:
            try:
                #Load program basics
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)
                ProgramNameRaw = ProgramName
                ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)

                #Check if there are search results
                if var.SearchFilterTerm != '':
                    searchMatch = func.search_filter_string(ProgramName)
                    searchResultFound = var.SearchFilterTerm in searchMatch
                    if searchResultFound == False: continue

                #Check if program has finished airing and processing
                if datetime.now() < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue

                #Check if program is available for streaming
                AssetsLength = len(program['assets'])
                if AssetsLength > 0:
                    AssetsStatus = str(program['assets'][0]['status'])
                    if AssetsStatus == 'RecordFailed':
                        ProgramName = '(Opname mislukt) ' + ProgramName
                    elif AssetsStatus == 'ScheduleSuccess':
                        ProgramName = '(Geplande opname) ' + ProgramName    
                else:
                    ProgramName = '(Niet speelbaar) ' + ProgramName

                #Load program details
                ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
                ProgramAssetId = metadatainfo.get_stream_assetid(program['assets'])
                ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
                EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(program, True, ProgramNameRaw)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
                ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(program)
                ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(program, False)
                ProgramDescription = metadatainfo.programdescription_from_json_metadata(program)
                ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(program))
                ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
                ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
                ProgramTimeStartStringTime = ProgramTimeStartDateTime.strftime('%H:%M')
                ProgramTimeStartStringDate = ProgramTimeStartDateTime.strftime('%a, %d %B %Y')
                ProgramTime = '[COLOR gray]Begon om ' + ProgramTimeStartStringTime + ' op ' + ProgramTimeStartStringDate + ' en duurde ' + ProgramDuration + '[/COLOR]'
                ProgramAvailability = metadatainfo.recording_available_time(program)

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
                listitem.setProperty('ProgramAssetId', ProgramAssetId)
                listitem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
                listitem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
                listitem.setProperty("ProgramName", ProgramName)
                listitem.setProperty("ProgramNameDesc", ProgramNameDesc)
                listitem.setProperty("ProgramNameRaw", ProgramNameRaw)
                listitem.setProperty("ProgramDetails", ProgramTime)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setInfo('video', {'Genre': 'Opname', 'Plot': ProgramDescription})
                listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the status
        self.count_program(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_event()
            var.guiMain.count_recording_event()

    #Update the status
    def count_program(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            if var.SearchFilterTerm != '':
                func.updateLabelText(self, 1, str(listcontainer.size()) + " gevonden opnames")
                func.updateLabelText(self, 3, "Zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR]")
            else:
                func.updateLabelText(self, 1, str(listcontainer.size()) + " opnames")
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
                func.updateLabelText(self, 1, 'Geen opnames gevonden')
                func.updateLabelText(self, 3, "Geen zoekresultaten voor [COLOR gray]" + var.SearchFilterTerm + "[/COLOR]")
                listcontainer.selectItem(1)
            else:
                func.updateLabelText(self, 1, 'Geen opnames')
                func.updateLabelText(self, 3, "")
                listcontainer.selectItem(0)
            xbmc.sleep(100)
