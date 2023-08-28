from datetime import datetime, timedelta
import alarm
import func
import metadatacombine
import metadatainfo

def list_update(listItem):
    #Get channel information from item
    ChannelId = listItem.getProperty('ChannelId')

    #Set the current player play time
    dateTimeNow = datetime.now()

    ProgramId = listItem.getProperty('ProgramId')
    ProgramNameProp = listItem.getProperty('ProgramName')
    ProgramDescriptionRaw = listItem.getProperty('ProgramDescriptionRaw')
    ProgramDetailsProp = listItem.getProperty('ProgramDetails')
    ProgramRecordSeriesId = listItem.getProperty('ProgramRecordSeriesId')
    ProgramTimeStartProp = listItem.getProperty('ProgramTimeStart')
    ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartProp, '%Y-%m-%d %H:%M:%S')
    ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
    ProgramTimeEndProp = listItem.getProperty('ProgramTimeEnd')
    ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndProp, '%Y-%m-%d %H:%M:%S')

    #Update program progress
    ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))

    #Combine program timing
    ProgramTimingList = metadatacombine.program_timing_program_property(listItem, dateTimeNow, True)
    ProgramTimingDescription = metadatacombine.program_timing_program_property(listItem, dateTimeNow, False)

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
    listItem.setProperty('ProgramEpgList', ProgramEpgList)
    listItem.setProperty('ProgramDescription', ProgramDescription)
    listItem.setProperty('ProgramAlarm', ProgramAlarm)
    listItem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
    listItem.setProperty('ProgramRecordEventPlanned', ProgramRecordEventPlanned)
    listItem.setProperty('ProgramRecordEventDone', ProgramRecordEventDone)
    listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
    listItem.setProperty('ProgramRecordSeries', ProgramRecordSeries)
    listItem.setProperty('ProgramProgressPercent', str(ProgramProgressPercent))
