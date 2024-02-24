from datetime import datetime, timedelta
import alarm
import download
import func
import getset
import metadatacombine
import metadatafunc
import metadatainfo
import var

def list_update(listItem):
    try:
        #Set the current player play time
        dateTimeNow = datetime.now()

        #Get channel information from item
        channelId = listItem.getProperty('ChannelId')
        channelName = listItem.getProperty('ChannelName')
        channelNumberAccent = listItem.getProperty('ChannelNumberAccent')

        #Get json epg from today
        epgTodayJson = download.download_epg_day(dateTimeNow, False)

        #Get json epg for the channelid
        channelEpg = metadatafunc.search_channelid_jsonepg(epgTodayJson, channelId)

        #Look for current airing program index
        programIndex = metadatafunc.search_programindex_airingtime_jsonepg(channelEpg, dateTimeNow)

        #Get the current program information
        try:
            #Load program basics
            metaData = channelEpg['containers'][programIndex]
            ProgramNowId = metadatainfo.contentId_from_json_metadata(metaData)
            ProgramNowName = metadatainfo.programtitle_from_json_metadata(metaData)

            #Load program timing
            ProgramNowTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
            ProgramNowTimeStartDateTime = func.datetime_remove_seconds(ProgramNowTimeStartDateTime)
            ProgramNowTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(metaData)
            ProgramProgressPercent = str(int(((dateTimeNow - ProgramNowTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramNowTimeEndDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60)))

            #Combine program timing
            ProgramNowTiming = metadatacombine.program_timing_program_metadata(metaData, dateTimeNow, dateTimeNow)

            #Combine program description extended
            ProgramNowDescription = metadatacombine.program_description_extended(metaData)

            #Combine program details
            ProgramNowDetails = metadatacombine.program_details(metaData, True, False, True, True, True, True, True)

            #Check if program is a rerun
            programRerunName = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramNowName.lower())
            programRerunDescription = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramNowDescription.lower())
            if programRerunName or programRerunDescription:
                ProgramNowRerun = 'true'
            else:
                ProgramNowRerun = 'false'

            #Check if program is recording event
            if metadatafunc.search_programid_jsonrecording_event(ProgramNowId):
                ProgramNowRecordEvent = 'true'
            else:
                ProgramNowRecordEvent = 'false'

            #Check if the program is part of series
            ProgramNowRecordSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

            #Check if program is recording series
            if metadatafunc.search_seriesid_jsonrecording_series(ProgramNowRecordSeriesId):
                ProgramNowRecordSeries = 'true'
            else:
                ProgramNowRecordSeries = 'false'
        except:
            ProgramNowId = ''
            ProgramNowRecordSeriesId = ''
            ProgramNowName = 'Onbekend programma'
            ProgramNowTiming = '[COLOR gray]onbekend programmaduur[/COLOR]'
            ProgramNowDescription = 'Programmabeschrijving is niet geladen of beschikbaar.'
            ProgramNowDetails = 'Onbekend seizoen en aflevering'
            ProgramNowTimeStartDateTime = datetime(1970,1,1)
            ProgramProgressPercent = '100'
            ProgramNowRerun = 'false'
            ProgramNowRecordEvent = 'false'
            ProgramNowRecordSeries = 'false'

        #Get the next program information
        try:
            metaData = channelEpg['containers'][programIndex + 1]
            ProgramNextId = metadatainfo.contentId_from_json_metadata(metaData)
            ProgramNextNameRaw = metadatainfo.programtitle_from_json_metadata(metaData)
            ProgramNextTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
            ProgramNextTimeStartDateTime = func.datetime_remove_seconds(ProgramNextTimeStartDateTime)
            ProgramNextTimeStartString = ProgramNextTimeStartDateTime.strftime('%H:%M')

            #Combine program next name
            ProgramNextName = '[COLOR gray]' + ProgramNextTimeStartString + ': ' + ProgramNextNameRaw + '[/COLOR]'

            #Check if program has active alarm
            if alarm.alarm_duplicate_program_check(ProgramNextTimeStartDateTime, channelId) == True:
                ProgramNextAlarm = 'true'
            else:
                ProgramNextAlarm = 'false'

            #Check if program is a rerun
            programRerunName = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramNextNameRaw.lower())
            if programRerunName:
                ProgramNextRerun = 'true'
            else:
                ProgramNextRerun = 'false'

            #Check if program is recording event
            if metadatafunc.search_programid_jsonrecording_event(ProgramNextId):
                ProgramNextRecordEvent = 'true'
            else:
                ProgramNextRecordEvent = 'false'

            #Check if the program is part of series
            ProgramNextRecordSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

            #Check if program is recording series
            if metadatafunc.search_seriesid_jsonrecording_series(ProgramNextRecordSeriesId):
                ProgramNextRecordSeries = 'true'
            else:
                ProgramNextRecordSeries = 'false'
        except:
            ProgramNextId = ''
            ProgramNextRecordSeriesId = ''
            ProgramNextName = '[COLOR gray]Onbekend programma[/COLOR]'
            ProgramNextNameRaw = 'Onbekend programma'
            ProgramNextTimeStartDateTime = datetime(1970,1,1)
            ProgramNextTimeStartString = 'Onbekend'
            ProgramNextAlarm = 'false'
            ProgramNextRerun = 'false'
            ProgramNextRecordEvent = 'false'
            ProgramNextRecordSeries = 'false'

        #Get upcoming programs information
        ProgramUpcoming = metadatacombine.program_upcoming_list(channelEpg['containers'], programIndex)

        #Get earlier programs information
        if getset.setting_get('TelevisionHideEarlierAired') == 'false':
            ProgramEarlier = metadatacombine.program_earlier_list(channelEpg['containers'], programIndex)
        else:
            ProgramEarlier = ''

        #Combine program description
        ProgramDescription = channelNumberAccent + ' ' + channelName + '\n\n' + ProgramNowName + ' ' + ProgramNowTiming + '\n\n' + ProgramNowDetails + '\n\n' + ProgramNowDescription

        #Append upcoming programs to the description
        if func.string_isnullorempty(ProgramUpcoming) == False:
            ProgramDescription += '\n\n' + ProgramUpcoming

        #Append earlier programs to the description
        if func.string_isnullorempty(ProgramEarlier) == False:
            ProgramDescription += '\n\n' + ProgramEarlier

        #Update the information in list item
        listItem.setProperty("ProgramNowId", ProgramNowId)
        listItem.setProperty("ProgramNowRecordSeriesId", ProgramNowRecordSeriesId)
        listItem.setProperty("ProgramNowName", ProgramNowName)
        listItem.setProperty("ProgramNowTimeStartDateTime", str(ProgramNowTimeStartDateTime))
        listItem.setProperty("ProgramDescription", ProgramDescription)
        listItem.setProperty("ProgramNextId", ProgramNextId)
        listItem.setProperty("ProgramNextRecordSeriesId", ProgramNextRecordSeriesId)
        listItem.setProperty("ProgramNextName", ProgramNextName)
        listItem.setProperty("ProgramNextNameRaw", ProgramNextNameRaw)
        listItem.setProperty("ProgramNextTimeStartDateTime", str(ProgramNextTimeStartDateTime))
        listItem.setProperty("ProgramNextAlarm", ProgramNextAlarm)
        listItem.setProperty("ProgramNowRerun", ProgramNowRerun)
        listItem.setProperty("ProgramNowRecordEvent", ProgramNowRecordEvent)
        listItem.setProperty("ProgramNowRecordSeries", ProgramNowRecordSeries)
        listItem.setProperty("ProgramNextRerun", ProgramNextRerun)
        listItem.setProperty("ProgramNextRecordEvent", ProgramNextRecordEvent)
        listItem.setProperty("ProgramNextRecordSeries", ProgramNextRecordSeries)
        listItem.setProperty("ProgramProgressPercent", ProgramProgressPercent)
    except:
        pass
