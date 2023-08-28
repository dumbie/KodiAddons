from datetime import datetime, timedelta
import alarm
import func
import metadatacombine
import metadatainfo

def list_update(updateItem):
    #Get channel information from item
    ChannelId = updateItem.getProperty('ChannelId')

    #Set the current player play time
    dateTimeNow = datetime.now()

    ProgramId = updateItem.getProperty('ProgramId')
    ProgramNameProp = updateItem.getProperty('ProgramName')
    ProgramDescriptionRaw = updateItem.getProperty('ProgramDescriptionRaw')
    ProgramDetailsProp = updateItem.getProperty('ProgramDetails')
    ProgramRecordSeriesId = updateItem.getProperty('ProgramRecordSeriesId')
    ProgramTimeStartProp = updateItem.getProperty('ProgramTimeStart')
    ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartProp, '%Y-%m-%d %H:%M:%S')
    ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
    ProgramTimeEndProp = updateItem.getProperty('ProgramTimeEnd')
    ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndProp, '%Y-%m-%d %H:%M:%S')

    #Update program progress
    ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))

    #Combine program timing
    ProgramTimingList = metadatacombine.program_timing_program_property(updateItem, dateTimeNow, True)
    ProgramTimingDescription = metadatacombine.program_timing_program_property(updateItem, dateTimeNow, False)

    #Check if program has active alarm
    if alarm.alarm_duplicate_program_check(ProgramTimeStartDateTime, ChannelId) == True:
        ProgramAlarm = 'true'
    else:
        ProgramAlarm = 'false'

    #Check if program is recording event and if the recording is planned or done
    recordProgramEvent = func.search_programid_jsonrecording_event(ProgramId)
    if recordProgramEvent:
        if dateTimeNow > ProgramTimeEndDateTime:
            ProgramRecordEventPlanned = 'false'
            ProgramRecordEventDone = 'true'
        else:
            ProgramRecordEventPlanned = 'true'
            ProgramRecordEventDone = 'false'
        ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
        ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent))
    else:
        ProgramRecordEventPlanned = 'false'
        ProgramRecordEventDone = 'false'
        ProgramRecordEventId = ''
        ProgramStartDeltaTime = '0'

    #Check if program is recording series
    recordProgramSeries = func.search_seriesid_jsonrecording_series(ProgramRecordSeriesId)
    if recordProgramSeries:
        ProgramRecordSeries = 'true'
    else:
        ProgramRecordSeries = 'false'

    #Combine the program description
    ProgramEpgList = ProgramTimeStartString + ' ' + ProgramTimingList
    ProgramDescription = ProgramNameProp + ' ' + ProgramTimingDescription + '\n\n' + ProgramDetailsProp + '\n\n' + ProgramDescriptionRaw

    #Update program list item
    updateItem.setProperty('ProgramEpgList', ProgramEpgList)
    updateItem.setProperty('ProgramDescription', ProgramDescription)
    updateItem.setProperty('ProgramAlarm', ProgramAlarm)
    updateItem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
    updateItem.setProperty('ProgramRecordEventPlanned', ProgramRecordEventPlanned)
    updateItem.setProperty('ProgramRecordEventDone', ProgramRecordEventDone)
    updateItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
    updateItem.setProperty('ProgramRecordSeries', ProgramRecordSeries)
    updateItem.setProperty('ProgramProgressPercent', str(ProgramProgressPercent))
