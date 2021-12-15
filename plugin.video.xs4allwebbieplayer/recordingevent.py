import json
from datetime import datetime, timedelta
import xbmc
import xbmcgui
import download
import func
import metadatainfo
import path
import var

def switch_to_page():
    if var.guiRecordingEvent == None:
        var.guiRecordingEvent = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiRecordingEvent.show()

def close_the_page():
    if var.guiRecordingEvent != None:
        #Close the shown window
        var.guiRecordingEvent.close()
        var.guiRecordingEvent = None

def count_main_recording():
    #Download the recording programs
    downloadResult = download.download_recording_event(False)
    if downloadResult == False: return '?'

    #Count planned recording
    recordingCount = 0
    for program in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
        try:
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)
            #Check if recording is planned or already recorded
            if ProgramTimeEndDateTime > datetime.now():
                recordingCount += 1
        except:
            continue
    return recordingCount

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        func.updateLabelText(self, 3000, 'Geplande Opnames')
        func.updateLabelText(self, 4001, 'Opnames vernieuwen')
        func.updateVisibility(self, 4001, True)

        #Load all current set recording
        self.load_recording(False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            ProgramRecordEventId = listItemSelected.getProperty("ProgramRecordEventId")
            ProgramStartDeltaTime = listItemSelected.getProperty("ProgramStartDeltaTime")
            recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramStartDeltaTime)
            if recordRemove == True:
                #Remove item from the list
                removeListItemId = clickedControl.getSelectedPosition()
                clickedControl.removeItem(removeListItemId)
                xbmc.sleep(100)
                clickedControl.selectItem(removeListItemId)
                xbmc.sleep(100)

                #Update the status
                self.count_recording(False)
        elif clickId == 4000:
            close_the_page()
        elif clickId == 4001:
            self.load_recording(True)

    def onAction(self, action):
        actionId = action.getId()
        if (actionId == var.ACTION_PREVIOUS_MENU or actionId == var.ACTION_BACKSPACE):
            close_the_page()

    def load_recording(self, forceUpdate=False):
        listcontainer = self.getControl(1000)
        listcontainer.reset()

        #Download the recording programs
        func.updateLabelText(self, 3001, "Geplande opnames worden gedownload.")
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 3001, 'Geplande opnames zijn niet beschikbaar')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
            return False

        #Sort recording by upcoming time
        func.updateLabelText(self, 3001, "Geplande opnames worden geladen.")
        RecordingEvents = var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]
        RecordingEvents = sorted(RecordingEvents, key=lambda x: x['metadata']['programStartTime'], reverse=False)

        #Process all the planned recording
        for program in RecordingEvents:
            try:
                #Load program basics
                ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)

                #Check if recording is planned or already recorded
                if ProgramTimeEndDateTime < datetime.now(): continue

                #Load program details
                ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
                ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
                ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(program))
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)
                ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
                ProgramYear = metadatainfo.programyear_from_json_metadata(program)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
                ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
                ProgramDescription = 'Van ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' tot ' + ProgramTimeEndDateTime.strftime('%H:%M') + ' op ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

                #Combine program details
                stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisode ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'

                #Update program name string
                ProgramName += ' [COLOR gray]' + ProgramDetails + '[/COLOR]'

                #Add recording event to the list
                listitem = xbmcgui.ListItem()
                listitem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
                listitem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
                listitem.setProperty('ProgramName', ProgramName)
                listitem.setProperty('ProgramDescription', ProgramDescription)
                listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the status
        self.count_recording(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recorded_event()
            var.guiMain.count_recording_event()

    #Update the status
    def count_recording(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            func.updateLabelText(self, 3000, 'Geplande Opnames (' + str(listcontainer.size()) + ')')
            func.updateLabelText(self, 3001, 'Huidig geplande programma opnames, u kunt een opname annuleren door er op te klikken.')
            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 3000, 'Geplande Opnames (0)')
            func.updateLabelText(self, 3001, 'Er zijn geen programma opnames gepland, u kunt een nieuwe opname plannen in de TV Gids of op de Televisie pagina.')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
