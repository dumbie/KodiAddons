import dialog
import download
import func
import metadatafunc
import metadatainfo
import var

def get_status(program):
    assetsArray = metadatainfo.stream_assets_array_from_json_metadata(program)
    if assetsArray != []:
        return metadatainfo.stream_assetstatus_from_assets_array(assetsArray)
    else:
        return 'NoAssets'

def check_status_recorded(program):
    recordingStatus = get_status(program)
    if recordingStatus == 'RecordFailed' or recordingStatus == 'RecordSuccess':
        return True
    else:
        return False

def check_status_scheduled(program):
    recordingStatus = get_status(program)
    if recordingStatus == 'ScheduleSuccess' or recordingStatus == 'RescheduleSuccess':
        return True
    else:
        return False

def count_recording_events():
    try:
        #Download the recording programs
        downloadResult = download.download_recording_event(False)
        if downloadResult == False: return '?'

        #Count planned recordings
        recordingCount = 0
        for program in var.RecordingEventDataJson["resultObj"]["containers"]:
            try:
                if check_status_scheduled(program) == True:
                    recordingCount += 1
            except:
                continue
        return recordingCount
    except:
        return '?'

def count_recorded_events():
    try:
        #Download the recording programs
        downloadResult = download.download_recording_event(False)
        if downloadResult == False: return '?'

        #Count finished recordings
        recordingCount = 0
        for program in var.RecordingEventDataJson["resultObj"]["containers"]:
            try:
                if check_status_recorded(program) == True:
                    recordingCount += 1
            except:
                continue
        return recordingCount
    except:
        return '?'

def count_recording_series():
    try:
        #Download the recording programs
        downloadResult = download.download_recording_series(False)
        if downloadResult == False: return '?'

        #Count planned recording
        return len(var.RecordingSeriesDataJson["resultObj"]["containers"])
    except:
        return '?'

def count_recorded_series_id(targetSeriesId):
    try:
        if var.RecordingEventDataJson == []: return ''

        #Count finished recordings
        recordedCount = 0
        for program in var.RecordingEventDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.seriesId_from_json_metadata(program) == targetSeriesId:
                    recordedCount += 1
            except:
                continue
        return '(' + str(recordedCount) + 'x)'
    except:
        return ''

def record_event_epg(_self, listItemSelected):
    ProgramId = listItemSelected.getProperty('ProgramId')

    #Check program recording state
    recordProgramEvent = metadatafunc.search_programid_jsonrecording_event(ProgramId)
    if recordProgramEvent:
        ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
        ProgramDeltaTimeStart = metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent)
        recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramDeltaTimeStart)
        if recordRemove == True:
            #Force manual epg update
            _self.ProgramManualUpdate = True
            _self.ChannelManualUpdate = True
    else:
        recordAdd = download.record_event_add(ProgramId)
        if func.string_isnullorempty(recordAdd) == False:
            #Force manual epg update
            _self.ProgramManualUpdate = True
            _self.ChannelManualUpdate = True

def record_event_now_television_playergui(listItemSelected):
    ProgramNowId = listItemSelected.getProperty('ProgramNowId')

    #Check program recording state
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

    #Check program recording state
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

def record_series_now_television_playergui(listItemSelected):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramNowSeriesId = listItemSelected.getProperty('ProgramNowSeriesId')
    ProgramNextSeriesId = listItemSelected.getProperty('ProgramNextSeriesId')

    #Check series recording state
    recordProgramSeries = metadatafunc.search_seriesid_jsonrecording_series(ProgramNowSeriesId)
    if recordProgramSeries:
        #Remove record series
        if record_series_remove_dialog(ProgramNowSeriesId) == True:
            listItemSelected.setProperty('ProgramNowRecordEvent', 'false')
            listItemSelected.setProperty('ProgramNowRecordSeries', 'false')
            if ProgramNextSeriesId == ProgramNowSeriesId:
                listItemSelected.setProperty('ProgramNextRecordEvent', 'false')
                listItemSelected.setProperty('ProgramNextRecordSeries', 'false')
    else:
        #Add record series
        if download.record_series_add(ChannelId, ProgramNowSeriesId) == True:
            listItemSelected.setProperty('ProgramNowRecordEvent', 'true')
            listItemSelected.setProperty('ProgramNowRecordSeries', 'true')
            if ProgramNextSeriesId == ProgramNowSeriesId:
                listItemSelected.setProperty('ProgramNextRecordEvent', 'true')
                listItemSelected.setProperty('ProgramNextRecordSeries', 'true')

def record_series_next_television_playergui(listItemSelected):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramNowSeriesId = listItemSelected.getProperty('ProgramNowSeriesId')
    ProgramNextSeriesId = listItemSelected.getProperty('ProgramNextSeriesId')

    #Check series recording state
    recordProgramSeries = metadatafunc.search_seriesid_jsonrecording_series(ProgramNextSeriesId)
    if recordProgramSeries:
        #Remove record series
        if record_series_remove_dialog(ProgramNextSeriesId) == True:
            listItemSelected.setProperty('ProgramNextRecordEvent', 'false')
            listItemSelected.setProperty('ProgramNextRecordSeries', 'false')
            if ProgramNextSeriesId == ProgramNowSeriesId:
                listItemSelected.setProperty('ProgramNowRecordEvent', 'false')
                listItemSelected.setProperty('ProgramNowRecordSeries', 'false')
    else:
        #Add record series
        if download.record_series_add(ChannelId, ProgramNextSeriesId) == True:
            listItemSelected.setProperty('ProgramNextRecordEvent', 'true')
            listItemSelected.setProperty('ProgramNextRecordSeries', 'true')
            if ProgramNextSeriesId == ProgramNowSeriesId:
                listItemSelected.setProperty('ProgramNowRecordEvent', 'true')
                listItemSelected.setProperty('ProgramNowRecordSeries', 'true')

def record_series_epg(_self, listItemSelected):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramSeriesId = listItemSelected.getProperty('ProgramSeriesId')

    #Check series recording state
    recordProgramSeries = metadatafunc.search_seriesid_jsonrecording_series(ProgramSeriesId)
    if recordProgramSeries:
        #Remove record series
        if record_series_remove_dialog(ProgramSeriesId) == True:
            #Force manual epg update
            _self.ProgramManualUpdate = True
            _self.ChannelManualUpdate = True
    else:
        #Add record series
        if download.record_series_add(ChannelId, ProgramSeriesId) == True:
            #Force manual epg update
            _self.ProgramManualUpdate = True
            _self.ChannelManualUpdate = True

def record_series_remove_dialog(seriesId):
    try:
        #Ask user to remove recordings
        dialogAnswers = ['Opnames verwijderen', 'Opnames houden']
        dialogHeader = 'Serie opnames verwijderen'
        dialogSummary = 'Wilt u ook alle opnames van deze serie seizoen verwijderen?'
        dialogFooter = ''
        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Opnames verwijderen':
            keepRecordings = False
        elif dialogResult == 'Opnames houden': 
            keepRecordings = True
        else:
            return False

        #Remove record series
        return download.record_series_remove(seriesId, keepRecordings)
    except:
        return False
