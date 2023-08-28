from datetime import datetime, timedelta
import alarm
import download
import func
import metadatacombine
import metadatainfo
import var
import xbmc

def list_update(updateItem):
    #Get channel information from item
    channelId = updateItem.getProperty('ChannelId')
    currentChannelId = var.addon.getSetting('CurrentChannelId')

    #Set the current player play time
    streamDelaySeconds = 15
    dateTimeNow = datetime.now()
    dateTimeSeek = dateTimeNow
    if channelId == currentChannelId:
        #Calculate current seek time
        playerSeekStepSizeHours = int(str(xbmc.getInfoLabel('Player.SeekTime(hh)'))) * 3600
        playerSeekStepSizeMinutes = int(str(xbmc.getInfoLabel('Player.SeekTime(mm)'))) * 60
        playerSeekStepSizeSeconds = int(str(xbmc.getInfoLabel('Player.SeekTime(ss)')))
        seekSeconds = playerSeekStepSizeHours + playerSeekStepSizeMinutes + playerSeekStepSizeSeconds + streamDelaySeconds

        #Calculate current player time
        totalSeconds = int(xbmc.Player().getTotalTime())
        playerSeconds = totalSeconds - seekSeconds

        #Set the current seek date time
        if seekSeconds - streamDelaySeconds > 1:
            dateTimeSeek -= timedelta(seconds=playerSeconds)

    try:
        #Get json epg from seek time
        epgSeekJson = download.download_epg_day(dateTimeSeek, False)

        #Get json epg for the channelid
        channelEpg = func.search_channelid_jsonepg(epgSeekJson, channelId)

        #Look for current airing program index
        programIndex = func.get_programindex_airingtime_jsonepg(channelEpg, dateTimeSeek)
    except:
        pass

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
        ProgramSeekPercent = str(int(((dateTimeSeek - ProgramNowTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramNowTimeEndDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60)))

        #Combine program timing
        ProgramNowTiming = metadatacombine.program_timing_program_metadata(metaData, dateTimeNow, dateTimeSeek)

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
        if func.search_programid_jsonrecording_event(ProgramNowId):
            ProgramNowRecordEvent = 'true'
        else:
            ProgramNowRecordEvent = 'false'

        #Check if the program is part of series
        ProgramNowRecordSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

        #Check if program is recording series
        if func.search_seriesid_jsonrecording_series(ProgramNowRecordSeriesId):
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
        ProgramNowTimeStartDateTime = datetime(1970, 1, 1)
        ProgramSeekPercent = '100'
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
        if func.search_programid_jsonrecording_event(ProgramNextId):
            ProgramNextRecordEvent = 'true'
        else:
            ProgramNextRecordEvent = 'false'

        #Check if the program is part of series
        ProgramNextRecordSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

        #Check if program is recording series
        if func.search_seriesid_jsonrecording_series(ProgramNextRecordSeriesId):
            ProgramNextRecordSeries = 'true'
        else:
            ProgramNextRecordSeries = 'false'
    except:
        ProgramNextId = ''
        ProgramNextRecordSeriesId = ''
        ProgramNextNameRaw = 'Onbekend programma'
        ProgramNextTimeStartDateTime = datetime(1970, 1, 1)
        ProgramNextTimeStartString = 'Onbekend'
        ProgramNextAlarm = 'false'
        ProgramNextRerun = 'false'
        ProgramNextRecordEvent = 'false'
        ProgramNextRecordSeries = 'false'

    #Combine program next name
    ProgramNextName = '[COLOR gray]' + ProgramNextTimeStartString + ': ' + ProgramNextNameRaw + '[/COLOR]'

    #Get upcoming programs information
    ProgramUpcoming = metadatacombine.program_upcoming_list(channelEpg['containers'], programIndex)

    #Get earlier programs information
    if var.addon.getSetting('TelevisionHideEarlierAired') == 'false':
        ProgramEarlier = metadatacombine.program_earlier_list(channelEpg['containers'], programIndex)
    else:
        ProgramEarlier = ''

    #Combine program description
    ProgramDescription = ProgramNowName + ' ' + ProgramNowTiming + '\n\n' + ProgramNowDetails + '\n\n' + ProgramNowDescription

    #Append upcoming programs to the description
    if func.string_isnullorempty(ProgramUpcoming) == False:
        ProgramDescription += '\n\n' + ProgramUpcoming

    #Append earlier programs to the description
    if func.string_isnullorempty(ProgramEarlier) == False:
        ProgramDescription += '\n\n' + ProgramEarlier

    #Update the information in list item
    updateItem.setProperty("ProgramNowId", ProgramNowId)
    updateItem.setProperty("ProgramNowRecordSeriesId", ProgramNowRecordSeriesId)
    updateItem.setProperty("ProgramNowName", ProgramNowName)
    updateItem.setProperty("ProgramNowTimeStartDateTime", str(ProgramNowTimeStartDateTime))
    updateItem.setProperty("ProgramDescription", ProgramDescription)
    updateItem.setProperty("ProgramNextId", ProgramNextId)
    updateItem.setProperty("ProgramNextRecordSeriesId", ProgramNextRecordSeriesId)
    updateItem.setProperty("ProgramNextName", ProgramNextName)
    updateItem.setProperty("ProgramNextNameRaw", ProgramNextNameRaw)
    updateItem.setProperty("ProgramNextTimeStartDateTime", str(ProgramNextTimeStartDateTime))
    updateItem.setProperty("ProgramNextAlarm", ProgramNextAlarm)
    updateItem.setProperty("ProgramNowRerun", ProgramNowRerun)
    updateItem.setProperty("ProgramNowRecordEvent", ProgramNowRecordEvent)
    updateItem.setProperty("ProgramNowRecordSeries", ProgramNowRecordSeries)
    updateItem.setProperty("ProgramNextRerun", ProgramNextRerun)
    updateItem.setProperty("ProgramNextRecordEvent", ProgramNextRecordEvent)
    updateItem.setProperty("ProgramNextRecordSeries", ProgramNextRecordSeries)
    updateItem.setProperty("ProgramSeekPercent", ProgramSeekPercent)
    updateItem.setProperty("ProgramProgressPercent", ProgramProgressPercent)
    updateItem.setInfo('video', {'Plot': ProgramDescription})
