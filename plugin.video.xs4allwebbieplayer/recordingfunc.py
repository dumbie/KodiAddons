from datetime import datetime, timedelta
import xbmcgui
import dialog
import download
import func
import metadatainfo
import metadatafunc
import path
import var

def count_recording_events():
    #Download the recording programs
    downloadResult = download.download_recording_event(False)
    if downloadResult == False: return '?'

    #Count planned recording
    recordingCount = 0
    for program in var.RecordingEventDataJson["resultObj"]["containers"]:
        try:
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)
            #Check if recording is planned or already recorded
            if ProgramTimeEndDateTime > datetime.now():
                recordingCount += 1
        except:
            continue
    return recordingCount

def count_recorded_events():
    #Download the recording programs
    downloadResult = download.download_recording_event(False)
    if downloadResult == False: return '?'

    #Count finished recordings
    recordingCount = 0
    for program in var.RecordingEventDataJson["resultObj"]["containers"]:
        try:
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)
            if datetime.now() < (ProgramTimeEndDateTime + timedelta(minutes=var.RecordingProcessMinutes)): continue
            recordingCount += 1
        except:
            continue
    return recordingCount

def count_recording_series():
    #Download the recording programs
    downloadResult = download.download_recording_series(False)
    if downloadResult == False: return '?'

    #Count planned recording
    return len(var.RecordingSeriesDataJson["resultObj"]["containers"])

def count_recorded_series_id(seriesId):
    try:
        if var.RecordingEventDataJson == []: return ''

        #Count finished recordings
        recordedCount = 0
        for program in var.RecordingEventDataJson["resultObj"]["containers"]:
            try:
                recordSeriesId = metadatainfo.seriesId_from_json_metadata(program)
                if recordSeriesId == seriesId:
                    recordedCount += 1
            except:
                continue
        return '(' + str(recordedCount) + 'x)'
    except:
        return ''

def record_event_epg(_self, listItemSelected, forceRecord=False):
    ProgramId = listItemSelected.getProperty('ProgramId')
    ProgramRecordEventId = listItemSelected.getProperty('ProgramRecordEventId')
    ProgramDeltaTimeStart = listItemSelected.getProperty('ProgramDeltaTimeStart')

    #Check if recording is already set
    if func.string_isnullorempty(ProgramRecordEventId) == True or forceRecord == True:
        recordAdd = download.record_event_add(ProgramId)
        if func.string_isnullorempty(recordAdd) == False:
            _self.update_channel_status()
            _self.update_program_status()
    else:
        recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramDeltaTimeStart)
        if recordRemove == True:
            _self.update_channel_status()
            _self.update_program_status()

def record_event_now_television_playergui(listItemSelected):
    ProgramNowId = listItemSelected.getProperty('ProgramNowId')

    #Check the program recording state
    recordProgramEvent = metadatafunc.search_programid_jsonrecording_event(ProgramNowId)
    if recordProgramEvent:
        ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
        ProgramDeltaTimeStart = metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent)
        recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramDeltaTimeStart)
        if recordRemove == True:
            listItemSelected.setProperty("ProgramNowRecordEvent", 'false')
    else:
        recordAdd = download.record_event_add(ProgramNowId)
        if func.string_isnullorempty(recordAdd) == False:
            listItemSelected.setProperty("ProgramNowRecordEvent", 'true')

def record_event_next_television_playergui(listItemSelected):
    ProgramNextId = listItemSelected.getProperty('ProgramNextId')

    #Check the program recording state
    recordProgramEvent = metadatafunc.search_programid_jsonrecording_event(ProgramNextId)
    if recordProgramEvent:
        ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
        ProgramDeltaTimeStart = metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent)
        recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramDeltaTimeStart)
        if recordRemove == True:
            listItemSelected.setProperty("ProgramNextRecordEvent", 'false')
    else:
        recordAdd = download.record_event_add(ProgramNextId)
        if func.string_isnullorempty(recordAdd) == False:
            listItemSelected.setProperty("ProgramNextRecordEvent", 'true')

def record_series_television_playergui(listItemSelected, forceRecord=False):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramNowRecordSeries = listItemSelected.getProperty('ProgramNowRecordSeries')
    ProgramNowRecordSeriesId = listItemSelected.getProperty('ProgramNowRecordSeriesId')
    ProgramNextRecordSeriesId = listItemSelected.getProperty('ProgramNextRecordSeriesId')

    if func.string_isnullorempty(ProgramNowRecordSeriesId) == True:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen kan niet worden opgenomen.', notificationIcon, 2500, False)
        return

    if ProgramNowRecordSeries == 'false' or forceRecord == True:
        seriesAdd = download.record_series_add(ChannelId, ProgramNowRecordSeriesId)
        if seriesAdd == True:
            listItemSelected.setProperty('ProgramNowRecordEvent', 'true')
            listItemSelected.setProperty('ProgramNowRecordSeries', 'true')
            if ProgramNextRecordSeriesId == ProgramNowRecordSeriesId:
                listItemSelected.setProperty('ProgramNextRecordEvent', 'true')
                listItemSelected.setProperty('ProgramNextRecordSeries', 'true')
    else:
        #Get the removal series id
        recordProgramSeries = metadatafunc.search_seriesid_jsonrecording_series(ProgramNowRecordSeriesId)
        if recordProgramSeries:
            ProgramRecordSeriesIdLive = metadatainfo.seriesId_from_json_metadata(recordProgramSeries)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt.', notificationIcon, 2500, False)
            return

        #Ask user to remove recordings
        dialogAnswers = ['Opnames verwijderen', 'Opnames houden']
        dialogHeader = 'Serie opnames verwijderen'
        dialogSummary = 'Wilt u ook alle opnames van deze serie seizoen verwijderen?'
        dialogFooter = ''
        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Opnames verwijderen':
            KeepRecording = False
        elif dialogResult == 'Opnames houden': 
            KeepRecording = True
        else:
            return

        #Remove record series
        seriesRemove = download.record_series_remove(ProgramRecordSeriesIdLive, KeepRecording)
        if seriesRemove == True:
            listItemSelected.setProperty('ProgramNowRecordEvent', 'false')
            listItemSelected.setProperty('ProgramNowRecordSeries', 'false')
            if ProgramNextRecordSeriesId == ProgramNowRecordSeriesId:
                listItemSelected.setProperty('ProgramNextRecordEvent', 'false')
                listItemSelected.setProperty('ProgramNextRecordSeries', 'false')

def record_series_epg(_self, listItemSelected, forceRecord=False):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramRecordSeries = listItemSelected.getProperty('ProgramRecordSeries')
    ProgramRecordSeriesId = listItemSelected.getProperty('ProgramRecordSeriesId')

    if func.string_isnullorempty(ProgramRecordSeriesId) == True:
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen kan niet worden opgenomen.', notificationIcon, 2500, False)
        return

    if ProgramRecordSeries == 'false' or forceRecord == True:
        seriesAdd = download.record_series_add(ChannelId, ProgramRecordSeriesId)
        if seriesAdd == True:
            _self.update_channel_status()
            _self.update_program_status()
    else:
        #Get the removal series id
        recordProgramSeries = metadatafunc.search_seriesid_jsonrecording_series(ProgramRecordSeriesId)
        if recordProgramSeries:
            ProgramRecordSeriesIdLive = metadatainfo.seriesId_from_json_metadata(recordProgramSeries)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt.', notificationIcon, 2500, False)
            return

        #Ask user to remove recordings
        dialogAnswers = ['Opnames verwijderen', 'Opnames houden']
        dialogHeader = 'Serie opnames verwijderen'
        dialogSummary = 'Wilt u ook alle opnames van deze serie seizoen verwijderen?'
        dialogFooter = ''
        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Opnames verwijderen':
            KeepRecording = False
        elif dialogResult == 'Opnames houden': 
            KeepRecording = True
        else:
            return

        #Remove record series
        seriesRemove = download.record_series_remove(ProgramRecordSeriesIdLive, KeepRecording)
        if seriesRemove == True:
            _self.update_channel_status()
            _self.update_program_status()
