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
    if var.guiRecordingSeries == None:
        var.guiRecordingSeries = Gui('schedule.xml', var.addonpath, 'default', '720p')
        var.guiRecordingSeries.show()

def close_the_page():
    if var.guiRecordingSeries != None:
        #Close the shown window
        var.guiRecordingSeries.close()
        var.guiRecordingSeries = None

def count_main_recording():
    #Download the recording programs
    downloadResult = download.download_recording_series(False)
    if downloadResult == False: return '?'

    #Count planned recording
    return len(var.ChannelsDataJsonRecordingSeries["resultObj"]["containers"])

def count_recorded_series(seriesId):
    try:
        if var.ChannelsDataJsonRecordingEvent == []: return ''
        recordedCount = 0
        for program in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
            try:
                recordSeriesId = metadatainfo.seriesId_from_json_metadata(program)
                if recordSeriesId == seriesId:
                    recordedCount += 1
            except:
                continue
        return '(' + str(recordedCount) + 'x)'
    except:
        return ''

class Gui(xbmcgui.WindowXMLDialog):
    def onInit(self):
        #Set the schedule window text
        func.updateLabelText(self, 3000, 'Geplande Series')
        func.updateLabelText(self, 4001, 'Series vernieuwen')
        func.updateVisibility(self, 4001, True)

        #Load all current set recording
        self.load_recording(False)

    def onClick(self, clickId):
        clickedControl = self.getControl(clickId)
        if clickId == 1000:
            listItemSelected = clickedControl.getSelectedItem()
            SeriesId = listItemSelected.getProperty('SeriesId')
            recordingRemoved = download.record_series_remove(SeriesId)
            if recordingRemoved == True:
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

        #Download the tv channels
        func.updateLabelText(self, 3001, 'Televisie zenders worden gedownload.')
        download.download_channels_tv(False)

        #Download the recording programs
        func.updateLabelText(self, 3001, "Geplande series worden gedownload.")
        downloadResult = download.download_recording_series(forceUpdate)
        if downloadResult == False:
            func.updateLabelText(self, 3001, 'Geplande series zijn niet beschikbaar')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
            return False

        #Process all the planned recording
        func.updateLabelText(self, 3001, "Geplande series worden geladen.")
        for program in var.ChannelsDataJsonRecordingSeries["resultObj"]["containers"]:
            try:
                #Load program basics
                ProgramSeriesId = metadatainfo.seriesId_from_json_metadata(program)
                ProgramName = metadatainfo.programtitle_from_json_metadata(program)

                #Check recorded episodes count
                ProgramEpisodeCount = count_recorded_series(ProgramSeriesId)

                #Get first recording event
                RecordingEvent = func.search_seriesid_jsonrecording_event(ProgramSeriesId)

                #Load program details
                ProgramYear = metadatainfo.programyear_from_json_metadata(RecordingEvent)
                ProgramSeason = metadatainfo.programseason_from_json_metadata(RecordingEvent)

                #Combine program details
                stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisodeCount ]
                ProgramDetails = ' '.join(filter(None, stringJoin))
                if func.string_isnullorempty(ProgramDetails):
                    ProgramDetails = '(?)'

                #Update program name string
                ProgramName += ' [COLOR gray]' + ProgramDetails + '[/COLOR]'

                #Get channel basics
                ChannelId = metadatainfo.channelId_from_json_metadata(program)
                ChannelName = 'Onbekende zender'
                ChannelIcon = path.resources('resources/skins/default/media/common/unknown.png')
                ChannelDetails = func.search_channelid_jsontelevision(ChannelId)
                if ChannelDetails:
                    ExternalId = metadatainfo.externalId_from_json_metadata(ChannelDetails)
                    ChannelName = metadatainfo.channelName_from_json_metadata(ChannelDetails)
                    ChannelIcon = path.icon_television(ExternalId)

                #Add recording series to the list
                listitem = xbmcgui.ListItem()
                listitem.setProperty('SeriesId', ProgramSeriesId)
                listitem.setProperty('ProgramName', ProgramName)
                listitem.setProperty('ProgramDescription', ChannelName)
                listitem.setArt({'thumb': ChannelIcon, 'icon': ChannelIcon})
                listcontainer.addItem(listitem)
            except:
                continue

        #Update the status
        self.count_recording(True)

        #Update the main page count
        if var.guiMain != None:
            var.guiMain.count_recording_series()

    #Update the status
    def count_recording(self, resetSelect=False):
        listcontainer = self.getControl(1000)
        if listcontainer.size() > 0:
            func.updateLabelText(self, 3000, 'Geplande Series (' + str(listcontainer.size()) + ')')
            func.updateLabelText(self, 3001, 'U kunt een serie seizoen annuleren door er op te klikken, alle opnames van dit seizoen zullen worden verwijderd.')
            if resetSelect == True:
                self.setFocus(listcontainer)
                xbmc.sleep(100)
                listcontainer.selectItem(0)
                xbmc.sleep(100)
        else:
            func.updateLabelText(self, 3000, 'Geplande Series (0)')
            func.updateLabelText(self, 3001, 'Er zijn geen serie seizoen opnames gepland, u kunt een nieuwe serie seizoen opnemen vanuit de TV Gids.')
            closeButton = self.getControl(4000)
            self.setFocus(closeButton)
            xbmc.sleep(100)
