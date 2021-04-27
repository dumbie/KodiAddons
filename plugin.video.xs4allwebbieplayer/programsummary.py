from datetime import datetime, timedelta
import alarm
import download
import func
import hybrid
import playergui
import metadatainfo
import var
import xbmc

#Generate program summary for playergui
def program_summary_playergui(updateItem):
    #Get channel information from item
    channelId = updateItem.getProperty('ChannelId')
    currentChannelId = var.addon.getSetting('CurrentChannelId')

    #Set the current player play time
    streamDelaySeconds = 15
    currentDateTime = datetime.now()
    currentSeekDateTime = currentDateTime
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
            currentSeekDateTime -= timedelta(seconds=playerSeconds)

    try:
        #Get json epg from today
        epgTodayJson = download.download_epg_day(currentDateTime.strftime('%Y-%m-%d'), False)

        #Get json epg for the channelid
        channelEpg = func.search_channelid_jsonepg(epgTodayJson, channelId)

        #Look for current airing program index
        programIndex = func.get_programindex_airingtime_jsonepg(channelEpg, currentSeekDateTime)
    except:
        pass

    #Get the current program information
    try:
        #Load program basics
        metaData = channelEpg['containers'][programIndex]
        ProgramNowId = metadatainfo.contentId_from_json_metadata(metaData)
        ProgramNowName = metadatainfo.programtitle_from_json_metadata(metaData)
        ProgramNowTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramNowTimeStartDateTime = func.datetime_remove_seconds(ProgramNowTimeStartDateTime)
        ProgramNowTimeStartString = ProgramNowTimeStartDateTime.strftime('%H:%M')
        ProgramNowTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(metaData)
        ProgramNowTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False, False)
        ProgramNowTimeLeftMinutes = int((ProgramNowTimeEndDateTime - currentSeekDateTime).total_seconds() / 60)
        ProgramNowTimeLeftString = str(ProgramNowTimeLeftMinutes)
        ProgramNowTimeEndString = (currentDateTime + timedelta(minutes=ProgramNowTimeLeftMinutes)).strftime('%H:%M')
        ProgramSeekPercent = str(int(((currentSeekDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramNowTimeEndDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60)))
        ProgramProgressPercent = str(int(((currentDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramNowTimeEndDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60)))

        #Load program details
        EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(metaData, True, ProgramNowName)
        ProgramYear = metadatainfo.programyear_from_json_metadata(metaData)
        ProgramSeason = metadatainfo.programseason_from_json_metadata(metaData)
        ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(metaData)
        ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(metaData)
        ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(metaData)
        ProgramGenres = metadatainfo.programgenres_from_json_metadata(metaData)
        ProgramNowDescription = metadatainfo.programdescription_from_json_metadata(metaData)

        #Combine program details
        stringJoin = [ EpisodeTitle, ProgramYear, ProgramSeason, ProgramEpisode, ProgramStarRating, ProgramAgeRating, ProgramGenres ]
        ProgramNowDetails = ' '.join(filter(None, stringJoin))
        if func.string_isnullorempty(ProgramNowDetails):
            ProgramNowDetails = 'Onbekend seizoen en aflevering'

        #Check if program is a rerun
        programRerunName = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramNowName.lower())
        programRerunDescription = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramNowDescription.lower())
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
        ProgramNowSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

        #Check if program is recording series
        if func.search_seriesid_jsonrecording_series(ProgramNowSeriesId):
            ProgramNowRecordSeries = 'true'
        else:
            ProgramNowRecordSeries = 'false'
    except:
        ProgramNowId = ''
        ProgramNowName = 'Onbekend programma'
        ProgramNowDescription = 'Programmabeschrijving is niet geladen of beschikbaar.'
        ProgramNowDetails = 'Onbekend seizoen en aflevering'
        ProgramNowTimeStartDateTime = datetime(1970, 1, 1)
        ProgramNowTimeStartString = 'Onbekend'
        ProgramNowTimeEndString = 'Onbekend'
        ProgramNowTimeDurationString = '0'
        ProgramNowTimeLeftString = '0'
        ProgramSeekPercent = '100'
        ProgramProgressPercent = '100'
        ProgramNowRerun = 'false'
        ProgramNowRecordEvent = 'false'
        ProgramNowRecordSeries = 'false'

    #Get the next program information
    try:
        metaData = channelEpg['containers'][programIndex + 1]
        ProgramNextId = metadatainfo.contentId_from_json_metadata(metaData)
        ProgramNextName = metadatainfo.programtitle_from_json_metadata(metaData)
        ProgramNextTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramNextTimeStartDateTime = func.datetime_remove_seconds(ProgramNextTimeStartDateTime)
        ProgramNextTimeStartString = ProgramNextTimeStartDateTime.strftime('%H:%M')

        #Check if program has active alarm
        if alarm.alarm_duplicate_program_check(ProgramNextTimeStartDateTime, channelId) == True:
            ProgramNextAlarm = 'true'
        else:
            ProgramNextAlarm = 'false'

        #Check if program is a rerun
        programRerunName = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramNextName.lower())
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
        ProgramNextSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

        #Check if program is recording series
        if func.search_seriesid_jsonrecording_series(ProgramNextSeriesId):
            ProgramNextRecordSeries = 'true'
        else:
            ProgramNextRecordSeries = 'false'
    except:
        ProgramNextId = ''
        ProgramNextName = 'Onbekend programma'
        ProgramNextTimeStartDateTime = datetime(1970, 1, 1)
        ProgramNextTimeStartString = 'Onbekend'
        ProgramNextAlarm = 'false'
        ProgramNextRerun = 'false'
        ProgramNextRecordEvent = 'false'
        ProgramNextRecordSeries = 'false'

    #Get upcoming programs information
    ProgramLater = '[COLOR gray]Later op deze zender:[/COLOR]'
    UpcomingProgramId = 1
    while UpcomingProgramId < 5:
        try:
            metaData = channelEpg['containers'][programIndex + UpcomingProgramId]
            ProgramLaterName = metadatainfo.programtitle_from_json_metadata(metaData)
            ProgramLaterTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
            ProgramLaterTimeStartString = ProgramLaterTimeStartDateTime.strftime('%H:%M')
            ProgramLaterTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False)
            ProgramLater += '\n[COLOR white]' + ProgramLaterTimeStartString + '/' + ProgramLaterTimeDurationString + '[/COLOR] [COLOR gray]' + ProgramLaterName + '[/COLOR]'
            UpcomingProgramId += 1
        except:
            break
    if ProgramLater == '[COLOR gray]Later op deze zender:[/COLOR]':
        ProgramLater = ''

    #Get earlier programs information
    ProgramEarlier = '[COLOR gray]Eerder op deze zender:[/COLOR]'
    UpcomingProgramId = 1
    while UpcomingProgramId < 5:
        try:
            metaData = channelEpg['containers'][programIndex - UpcomingProgramId]
            ProgramLaterName = metadatainfo.programtitle_from_json_metadata(metaData)
            ProgramLaterTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
            ProgramLaterTimeStartString = ProgramLaterTimeStartDateTime.strftime('%H:%M')
            ProgramLaterTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False)
            ProgramEarlier += '\n[COLOR white]' + ProgramLaterTimeStartString + '/' + ProgramLaterTimeDurationString + '[/COLOR] [COLOR gray]' + ProgramLaterName + '[/COLOR]'
            UpcomingProgramId += 1
        except:
            break
    if ProgramEarlier == '[COLOR gray]Eerder op deze zender:[/COLOR]':
        ProgramEarlier = ''

    #Combine the program timing
    if ProgramNowTimeDurationString == '0':
        ProgramTiming = ProgramNowName
    elif ProgramNowTimeLeftString == '0':
        ProgramTiming = ProgramNowName + ' is bijna afgelopen, duurde ' + ProgramNowTimeDurationString + ' minuten en begon om ' + ProgramNowTimeStartString
    else:
        ProgramTiming = ProgramNowName + ' duurt nog ' + ProgramNowTimeLeftString + ' van de ' + ProgramNowTimeDurationString + ' minuten, begon om ' + ProgramNowTimeStartString + ' eindigt rond ' + ProgramNowTimeEndString

    #Combine the program description
    ProgramDescription = '[COLOR white]' + ProgramTiming + '[/COLOR]\n\n[COLOR gray]' + ProgramNowDetails + '[/COLOR]\n\n[COLOR white]' + ProgramNowDescription + '[/COLOR]'

    #Append later programs to the description
    if func.string_isnullorempty(ProgramLater) == False:
        ProgramDescription += '\n\n' + ProgramLater

    #Append earlier programs to the description
    if func.string_isnullorempty(ProgramEarlier) == False:
        ProgramDescription += '\n\n' + ProgramEarlier

    #Update the information in list item
    updateItem.setProperty("ProgramNowId", ProgramNowId)
    updateItem.setProperty("ProgramNowName", ProgramNowName)
    updateItem.setProperty("ProgramDescription", ProgramDescription)
    updateItem.setProperty("ProgramNowTimeStartDateTime", str(ProgramNowTimeStartDateTime))
    updateItem.setProperty("ProgramNextId", ProgramNextId)
    updateItem.setProperty("ProgramNextName", ProgramNextTimeStartString + ': ' + ProgramNextName)
    updateItem.setProperty("ProgramNextNameRaw", ProgramNextName)
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

#Generate program summary for television
def program_summary_television(updateItem):
    #Get channel information from item
    channelId = updateItem.getProperty('ChannelId')
    channelName = updateItem.getProperty('ChannelName')

    #Set the current player play time
    currentDateTime = datetime.now()

    try:
        #Get json epg from today
        epgTodayJson = download.download_epg_day(currentDateTime.strftime('%Y-%m-%d'), False)

        #Get json epg for the channelid
        channelEpg = func.search_channelid_jsonepg(epgTodayJson, channelId)

        #Look for current airing program index
        programIndex = func.get_programindex_airingtime_jsonepg(channelEpg, currentDateTime)
    except:
        pass

    #Get the current program information
    try:
        #Load program basics
        metaData = channelEpg['containers'][programIndex]
        ProgramNowId = metadatainfo.contentId_from_json_metadata(metaData)
        ProgramNowName = metadatainfo.programtitle_from_json_metadata(metaData)
        ProgramNowTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramNowTimeStartDateTime = func.datetime_remove_seconds(ProgramNowTimeStartDateTime)
        ProgramNowTimeStartString = ProgramNowTimeStartDateTime.strftime('%H:%M')
        ProgramNowTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(metaData)
        ProgramNowTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False, False)
        ProgramNowTimeLeftMinutes = int((ProgramNowTimeEndDateTime - currentDateTime).total_seconds() / 60)
        ProgramNowTimeLeftString = str(ProgramNowTimeLeftMinutes)
        ProgramNowTimeEndString = ProgramNowTimeEndDateTime.strftime('%H:%M')
        ProgramProgressPercent = str(int(((currentDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramNowTimeEndDateTime - ProgramNowTimeStartDateTime).total_seconds() / 60)))

        #Load program details
        EpisodeTitle = metadatainfo.episodetitle_from_json_metadata(metaData, True, ProgramNowName)
        ProgramYear = metadatainfo.programyear_from_json_metadata(metaData)
        ProgramSeason = metadatainfo.programseason_from_json_metadata(metaData)
        ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(metaData)
        ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(metaData)
        ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(metaData)
        ProgramGenres = metadatainfo.programgenres_from_json_metadata(metaData)
        ProgramNowDescription = metadatainfo.programdescription_from_json_metadata(metaData)

        #Combine program details
        stringJoin = [ EpisodeTitle, ProgramYear, ProgramSeason, ProgramEpisode, ProgramStarRating, ProgramAgeRating, ProgramGenres ]
        ProgramNowDetails = ' '.join(filter(None, stringJoin))
        if func.string_isnullorempty(ProgramNowDetails):
            ProgramNowDetails = 'Onbekend seizoen en aflevering'

        #Check if program is a rerun
        programRerunName = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramNowName.lower())
        programRerunDescription = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramNowDescription.lower())
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
        ProgramNowSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

        #Check if program is recording series
        if func.search_seriesid_jsonrecording_series(ProgramNowSeriesId):
            ProgramNowRecordSeries = 'true'
        else:
            ProgramNowRecordSeries = 'false'
    except:
        ProgramNowId = ''
        ProgramNowName = 'Onbekend programma'
        ProgramNowDescription = 'Programmabeschrijving is niet geladen of beschikbaar.'
        ProgramNowDetails = 'Onbekend seizoen en aflevering'
        ProgramNowTimeStartDateTime = datetime(1970, 1, 1)
        ProgramNowTimeStartString = 'Onbekend'
        ProgramNowTimeEndString = 'Onbekend'
        ProgramNowTimeDurationString = '0'
        ProgramNowTimeLeftString = '0'
        ProgramProgressPercent = '100'
        ProgramNowRerun = 'false'
        ProgramNowRecordEvent = 'false'
        ProgramNowRecordSeries = 'false'

    #Get the next program information
    try:
        metaData = channelEpg['containers'][programIndex + 1]
        ProgramNextId = metadatainfo.contentId_from_json_metadata(metaData)
        ProgramNextName = metadatainfo.programtitle_from_json_metadata(metaData)
        ProgramNextTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramNextTimeStartDateTime = func.datetime_remove_seconds(ProgramNextTimeStartDateTime)
        ProgramNextTimeStartString = ProgramNextTimeStartDateTime.strftime('%H:%M')

        #Check if program has active alarm
        if alarm.alarm_duplicate_program_check(ProgramNextTimeStartDateTime, channelId) == True:
            ProgramNextAlarm = 'true'
        else:
            ProgramNextAlarm = 'false'

        #Check if program is a rerun
        programRerunName = any(substring for substring in var.EpgRerunSearchTerm if substring in ProgramNextName.lower())
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
        ProgramNextSeriesId = metadatainfo.seriesId_from_json_metadata(metaData)

        #Check if program is recording series
        if func.search_seriesid_jsonrecording_series(ProgramNextSeriesId):
            ProgramNextRecordSeries = 'true'
        else:
            ProgramNextRecordSeries = 'false'
    except:
        ProgramNextId = ''
        ProgramNextName = 'Onbekend programma'
        ProgramNextTimeStartDateTime = datetime(1970, 1, 1)
        ProgramNextTimeStartString = 'Onbekend'
        ProgramNextAlarm = 'false'
        ProgramNextRerun = 'false'
        ProgramNextRecordEvent = 'false'
        ProgramNextRecordSeries = 'false'

    #Get upcoming programs information
    ProgramLater = '[COLOR gray]Later op deze zender:[/COLOR]'
    UpcomingProgramId = 1
    while UpcomingProgramId < 5:
        try:
            metaData = channelEpg['containers'][programIndex + UpcomingProgramId]
            ProgramLaterName = metadatainfo.programtitle_from_json_metadata(metaData)
            ProgramLaterTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
            ProgramLaterTimeStartString = ProgramLaterTimeStartDateTime.strftime('%H:%M')
            ProgramLaterTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False)
            ProgramLater += '\n[COLOR white]' + ProgramLaterTimeStartString + '/' + ProgramLaterTimeDurationString + '[/COLOR] [COLOR gray]' + ProgramLaterName + '[/COLOR]'
            UpcomingProgramId += 1
        except:
            break
    if ProgramLater == '[COLOR gray]Later op deze zender:[/COLOR]':
        ProgramLater = ''

    #Get earlier programs information
    ProgramEarlier = '[COLOR gray]Eerder op deze zender:[/COLOR]'
    UpcomingProgramId = 1
    while UpcomingProgramId < 5:
        try:
            metaData = channelEpg['containers'][programIndex - UpcomingProgramId]
            ProgramLaterName = metadatainfo.programtitle_from_json_metadata(metaData)
            ProgramLaterTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
            ProgramLaterTimeStartString = ProgramLaterTimeStartDateTime.strftime('%H:%M')
            ProgramLaterTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False)
            ProgramEarlier += '\n[COLOR white]' + ProgramLaterTimeStartString + '/' + ProgramLaterTimeDurationString + '[/COLOR] [COLOR gray]' + ProgramLaterName + '[/COLOR]'
            UpcomingProgramId += 1
        except:
            break
    if ProgramEarlier == '[COLOR gray]Eerder op deze zender:[/COLOR]':
        ProgramEarlier = ''

    #Combine the program timing
    if ProgramNowTimeDurationString == '0':
        ProgramTiming = channelName + '\n\n' + ProgramNowName
    elif ProgramNowTimeLeftString == '0':
        ProgramTiming = channelName + '\n\n' + ProgramNowName + ' is bijna afgelopen, duurde ' + ProgramNowTimeDurationString + ' minuten en begon om ' + ProgramNowTimeStartString
    else:
        ProgramTiming = channelName + '\n\n' + ProgramNowName + ' duurt nog ' + ProgramNowTimeLeftString + ' van de ' + ProgramNowTimeDurationString + ' minuten, begon om ' + ProgramNowTimeStartString + ' eindigt rond ' + ProgramNowTimeEndString

    #Combine the program description
    ProgramDescription = '[COLOR white]' + ProgramTiming + '[/COLOR]\n\n[COLOR gray]' + ProgramNowDetails + '[/COLOR]\n\n[COLOR white]' + ProgramNowDescription + '[/COLOR]'

    #Append later programs to the description
    if func.string_isnullorempty(ProgramLater) == False:
        ProgramDescription += '\n\n' + ProgramLater

    #Append earlier programs to the description
    if func.string_isnullorempty(ProgramEarlier) == False:
        ProgramDescription += '\n\n' + ProgramEarlier

    #Update the information in list item
    updateItem.setProperty("ProgramNowId", ProgramNowId)
    updateItem.setProperty("ProgramNowName", ProgramNowName)
    updateItem.setProperty("ProgramDescription", ProgramDescription)
    updateItem.setProperty("ProgramNextId", ProgramNextId)
    updateItem.setProperty("ProgramNextName", ProgramNextTimeStartString + ': ' + ProgramNextName)
    updateItem.setProperty("ProgramNextNameRaw", ProgramNextName)
    updateItem.setProperty("ProgramNextTimeStartDateTime", str(ProgramNextTimeStartDateTime))
    updateItem.setProperty("ProgramNextAlarm", ProgramNextAlarm)
    updateItem.setProperty("ProgramNowRerun", ProgramNowRerun)
    updateItem.setProperty("ProgramNowRecordEvent", ProgramNowRecordEvent)
    updateItem.setProperty("ProgramNowRecordSeries", ProgramNowRecordSeries)
    updateItem.setProperty("ProgramNextRerun", ProgramNextRerun)
    updateItem.setProperty("ProgramNextRecordEvent", ProgramNextRecordEvent)
    updateItem.setProperty("ProgramNextRecordSeries", ProgramNextRecordSeries)
    updateItem.setProperty("ProgramProgressPercent", ProgramProgressPercent)
    updateItem.setInfo('video', {'Plot': ProgramDescription})
