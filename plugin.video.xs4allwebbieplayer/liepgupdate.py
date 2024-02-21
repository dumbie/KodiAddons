from datetime import datetime, timedelta
import alarm
import func
import metadatacombine
import metadatafunc
import metadatainfo

def list_update_channel(listItem):
    try:
        ChannelId = listItem.getProperty('ChannelId')

        #Check if channel has active alarm
        if alarm.alarm_duplicate_channel_check(ChannelId) == True:
            ChannelAlarm = 'true'
        else:
            ChannelAlarm = 'false'

        #Check if channel has active recording
        if metadatafunc.search_channelid_jsonrecording_event(ChannelId, True):
            ChannelRecordEvent = 'true'
        else:
            ChannelRecordEvent = 'false'

        #Check if channel has active recording series
        if metadatafunc.search_channelid_jsonrecording_series(ChannelId):
            ChannelRecordSeries = 'true'
        else:
            ChannelRecordSeries = 'false'

        #Update channel list item
        listItem.setProperty('ChannelAlarm', ChannelAlarm)
        listItem.setProperty('ChannelRecordEvent', ChannelRecordEvent)
        listItem.setProperty('ChannelRecordSeries', ChannelRecordSeries)
    except:
        pass

def list_update_program(listItem):
    try:
        #Set the current player play time
        dateTimeNow = datetime.now()

        #Get channel information from item
        ChannelId = listItem.getProperty('ChannelId')

        #Get program information from item
        ProgramId = listItem.getProperty('ProgramId')
        ProgramName = listItem.getProperty('ProgramName')
        ProgramDescriptionRaw = listItem.getProperty('ProgramDescriptionRaw')
        ProgramIsCatchup = listItem.getProperty('ProgramIsCatchup')
        ProgramDetails = listItem.getProperty('ProgramDetails')
        ProgramRecordSeriesId = listItem.getProperty('ProgramRecordSeriesId')
        ProgramTimeStart = listItem.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStart, '%Y-%m-%d %H:%M:%S')
        ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
        ProgramTimeEnd = listItem.getProperty('ProgramTimeEnd')
        ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEnd, '%Y-%m-%d %H:%M:%S')

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
        recordProgramEvent = metadatafunc.search_programid_jsonrecording_event(ProgramId)
        if recordProgramEvent:
            if dateTimeNow > ProgramTimeEndDateTime:
                ProgramRecordEventPlanned = 'false'
                ProgramRecordEventDone = 'true'
            else:
                ProgramRecordEventPlanned = 'true'
                ProgramRecordEventDone = 'false'
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
            ProgramDeltaTimeStart = str(metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent))
        else:
            ProgramRecordEventPlanned = 'false'
            ProgramRecordEventDone = 'false'
            ProgramRecordEventId = ''
            ProgramDeltaTimeStart = '0'

        #Check if program is recording series
        recordProgramSeries = metadatafunc.search_seriesid_jsonrecording_series(ProgramRecordSeriesId)
        if recordProgramSeries:
            ProgramRecordSeries = 'true'
        else:
            ProgramRecordSeries = 'false'

        #Combine the program description
        ProgramEpgList = ProgramTimeStartString + ' ' + ProgramTimingList
        ProgramDescriptionDesc = ProgramName + ' ' + ProgramTimingDescription + '\n\n' + ProgramDetails + '\n\n' + ProgramDescriptionRaw

        #Check if program is still to come
        if ProgramProgressPercent <= 0:
            listItem.setProperty('ProgramIsUpcoming', 'true')

        #Check if program finished airing
        if ProgramProgressPercent >= 100:
            #Set program available status
            listItem.setProperty('ProgramIsAvailable', ProgramIsCatchup)

            #Set program seek offset start
            StartOffset = str(int(func.setting_get('PlayerSeekOffsetStartMinutes')) * 60)
            listItem.setProperty('StartOffset', StartOffset)

        #Check if program is currently airing
        if ProgramProgressPercent > 0 and ProgramProgressPercent < 100:
            #Set program airing status
            listItem.setProperty('ProgramIsAiring', 'true')

            #Set channel stream asset identifier
            channelJson = metadatafunc.search_channelid_jsontelevision(ChannelId)
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(channelJson)
            listItem.setProperty('StreamAssetId', StreamAssetId)

        #Update program list item
        listItem.setProperty('ProgramEpgList', ProgramEpgList)
        listItem.setProperty('ProgramDescriptionDesc', ProgramDescriptionDesc)
        listItem.setProperty('ProgramAlarm', ProgramAlarm)
        listItem.setProperty('ProgramDeltaTimeStart', ProgramDeltaTimeStart)
        listItem.setProperty('ProgramRecordEventPlanned', ProgramRecordEventPlanned)
        listItem.setProperty('ProgramRecordEventDone', ProgramRecordEventDone)
        listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
        listItem.setProperty('ProgramRecordSeries', ProgramRecordSeries)
        listItem.setProperty('ProgramProgressPercent', str(ProgramProgressPercent))
    except:
        pass
