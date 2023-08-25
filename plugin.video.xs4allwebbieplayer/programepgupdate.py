from datetime import datetime, timedelta
import alarm
import func
import metadatainfo

def list_update(updateItem):
    #Get channel information from item
    ChannelId = updateItem.getProperty('ChannelId')

    #Set the current player play time
    dateTimeNow = datetime.now()

    ProgramId = updateItem.getProperty('ProgramId')
    ProgramName = updateItem.getProperty('ProgramName')
    ProgramDescriptionRaw = updateItem.getProperty('ProgramDescriptionRaw')
    ProgramDetailsProp = updateItem.getProperty('ProgramDetails')
    ProgramRecordSeriesId = updateItem.getProperty('ProgramRecordSeriesId')
    ProgramTimeStartProp = updateItem.getProperty('ProgramTimeStart')
    ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartProp, '%Y-%m-%d %H:%M:%S')
    ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
    ProgramTimeEndProp = updateItem.getProperty('ProgramTimeEnd')
    ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndProp, '%Y-%m-%d %H:%M:%S')
    ProgramTimeEndString = ProgramTimeEndDateTime.strftime('%H:%M')
    ProgramTimeLeftMinutes = int((ProgramTimeEndDateTime - dateTimeNow).total_seconds() / 60)
    ProgramTimeLeftString = str(ProgramTimeLeftMinutes)
    ProgramDurationString = updateItem.getProperty('ProgramDuration')

    #Update program progress
    ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))

    #Set program duration text
    if ProgramDurationString == '0':
        ProgramTimingEpgList = ' onbekend programmaduur'
        ProgramTimingDescription = ' [COLOR gray]onbekend programmaduur[/COLOR]'
    if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
        if ProgramTimeLeftString == '0':
            ProgramTimingEpgList = ' is bijna afgelopen, duurde ' + ProgramDurationString + ' minuten'
            ProgramTimingDescription = ' [COLOR gray]is bijna afgelopen, duurde[/COLOR] ' + ProgramDurationString + ' [COLOR gray]minuten, begon om[/COLOR] ' + ProgramTimeStartString
        else:
            ProgramTimingEpgList = ' duurt nog ' + ProgramTimeLeftString + ' van de ' + ProgramDurationString + ' minuten'
            ProgramTimingDescription = ' [COLOR gray]duurt nog[/COLOR] ' + ProgramTimeLeftString + ' [COLOR gray]van de[/COLOR] ' + ProgramDurationString + ' [COLOR gray]minuten, begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR gray]eindigt rond[/COLOR] ' + ProgramTimeEndString
    elif dateTimeNow > ProgramTimeEndDateTime:
        ProgramTimingEpgList = ' duurde ' + ProgramDurationString + ' minuten'
        ProgramTimingDescription = ' [COLOR gray]duurde[/COLOR] ' + ProgramDurationString + ' [COLOR gray]minuten, begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR gray]eindigde rond[/COLOR] ' + ProgramTimeEndString
    else:
        ProgramTimingEpgList = ' duurt ' + ProgramDurationString + ' minuten'
        ProgramTimingDescription = ' [COLOR gray]duurt[/COLOR] ' + ProgramDurationString + ' [COLOR gray]minuten, begint om[/COLOR] ' + ProgramTimeStartString + ' [COLOR gray]eindigt rond[/COLOR] ' + ProgramTimeEndString

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
    ProgramEpgList = ProgramTimeStartString + ProgramTimingEpgList
    ProgramDescription = '[COLOR white]' + ProgramName + ProgramTimingDescription + '[/COLOR]\n\n[COLOR gray]' + ProgramDetailsProp + '[/COLOR]\n\n[COLOR white]' + ProgramDescriptionRaw + '[/COLOR]'

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
