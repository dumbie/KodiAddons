from datetime import datetime, timedelta
import func
import hybrid
import var

#Get channel id from json metadata
def channelId_from_json_metadata(metaData):
    try:
        if 'channelId' in metaData['metadata']:
            return str(metaData['metadata']['channelId'])
        if 'channelId' in metaData['channel']:
            return str(metaData['channel']['channelId'])
        return ''
    except:
        return ''

#Get channel name from json metadata
def channelName_from_json_metadata(metaData):
    try:
        #Get the channel name
        if 'channelName' in metaData['metadata']:
            channelNameString = metaData['metadata']['channelName']
        elif 'channelName' in metaData['channel']:
            channelNameString = metaData['channel']['channelName']

        #Convert channel name string
        channelNameString = hybrid.unicode_to_string(channelNameString)
        channelNameString = hybrid.htmlparser_unescape(channelNameString)

        #Check the channel name
        if func.string_isnullorempty(channelNameString):
            channelNameString = "Onbekende zender"

        return str(channelNameString)
    except:
        return "Onbekende zender"

#Get content id from json metadata
def contentId_from_json_metadata(metaData):
    try:
        if 'contentId' in metaData['metadata']:
            return str(metaData['metadata']['contentId'])
        return ''
    except:
        return ''

#Get content id live from json metadata
def contentIdLive_from_json_metadata(metaData):
    try:
        if 'liveContentId' in metaData['metadata']:
            return str(metaData['metadata']['liveContentId'])
        return ''
    except:
        return ''

#Get series id from json metadata
def seriesId_from_json_metadata(metaData):
    try:
        if 'seriesId' in metaData['metadata']:
            return str(metaData['metadata']['seriesId'])
        return ''
    except:
        return ''

#Get series id live from json metadata
def seriesIdLive_from_json_metadata(metaData):
    try:
        if 'liveSeriesId' in metaData['metadata']:
            return str(metaData['metadata']['liveSeriesId'])
        return ''
    except:
        return ''

#Get order id from json metadata
def orderId_from_json_metadata(metaData):
    try:
        return str(metaData['metadata']['orderId'])
    except:
        return '9000'

#Get external id from json metadata
def externalId_from_json_metadata(metaData):
    try:
        return str(metaData['metadata']['externalId'])
    except:
        return 'unknown'

#Get external channel id from json metadata
def externalChannelId_from_json_metadata(metaData):
    try:
        if 'externalChannelId' in metaData['metadata']:
            return str(metaData['metadata']['externalChannelId'])
        if 'externalChannelId' in metaData['channel']:
            return str(metaData['channel']['externalChannelId'])
        return 'unknown'
    except:
        return 'unknown'

#Get contentSubtype from json metadata
def contentSubtype_from_json_metadata(metaData):
    try:
        return str(metaData['metadata']['contentSubtype'])
    except:
        return 'unknown'

#Get picture url from json metadata
def pictureUrl_from_json_metadata(metaData):
    try:
        return str(metaData['metadata']['pictureUrl'])
    except:
        return 'unknown'

#Get contentOptions from json metadata
def contentOptions_from_json_metadata(metaData):
    try:
        return metaData["metadata"]["contentOptions"]
    except:
        return []

#Get technical packages from json metadata
def technicalPackageIds_from_json_metadata(metaData):
    try:
        return metaData['technicalPackageIds']
    except:
        return []

#Get program title from json metadata
def programtitle_from_json_metadata(metaData, stripTitle=False):
    try:
        programNameString = metaData['metadata']['title']
        programNameString = hybrid.unicode_to_string(programNameString)
        programNameString = hybrid.htmlparser_unescape(programNameString)

        #Check the program name
        if func.string_isnullorempty(programNameString):
            programNameString = 'Onbekend programma'

        #Strip the program name
        if stripTitle:
            for stripString in var.ProgramTitleStripStrings:
                programNameString = func.string_replace_insensitive(stripString, '', programNameString)
            for stripRegEx in var.ProgramTitleStripRegEx:
                programNameString = func.string_replace_regex(stripRegEx, '', programNameString)

        return str(programNameString)
    except:
        return 'Onbekend programma'

#Get program startdelta from json metadata
def programstartdeltatime_from_json_metadata(metaData):
    try:
        return int(metaData['metadata']['startDeltaTime'])
    except:
        return 0

#Get program starttime from json metadata
def programstarttime_from_json_metadata(metaData):
    try:
        if 'airingStartTime' in metaData['metadata']:
            return int(metaData['metadata']['airingStartTime'])
        if 'programStartTime' in metaData['metadata']:
            return int(metaData['metadata']['programStartTime'])
        return 0
    except:
        return 0

#Get program starttime from json metadata
def programstartdatetime_from_json_metadata(metaData):
    try:
        if 'airingStartTime' in metaData['metadata']:
            return func.datetime_from_ticks(int(metaData['metadata']['airingStartTime']))
        if 'programStartTime' in metaData['metadata']:
            return func.datetime_from_ticks(int(metaData['metadata']['programStartTime']))
        return datetime(1970, 1, 1)
    except:
        return datetime(1970, 1, 1)

#Get program endtime from json metadata
def programenddatetime_from_json_metadata(metaData):
    try:
        if 'airingEndTime' in metaData['metadata']:
            return func.datetime_from_ticks(int(metaData['metadata']['airingEndTime']))
        if 'programEndTime' in metaData['metadata']:
            return func.datetime_from_ticks(int(metaData['metadata']['programEndTime']))
        return datetime(1970, 1, 1)
    except:
        return datetime(1970, 1, 1)

#Get contract endtime from json metadata
def contractenddatetime_from_json_metadata(metaData):
    try:
        return func.datetime_from_ticks(int(metaData['metadata']['contractEndDate']))
    except:
        return datetime(1970, 1, 1)

#Generate program endtime from json metadata
def programenddatetime_generate_from_json_metadata(metaData):
    try:
        programStartTimeTicks = int(metaData['metadata']['programStartTime'])
        programDurationTicks = int(metaData['metadata']['programDuration']) * 1000
        programTimeEndTicks = int(programStartTimeTicks + programDurationTicks)
        return func.datetime_from_ticks(programTimeEndTicks)
    except:
        return datetime(1970, 1, 1)

#Get program duration from json metadata
def programdurationint_from_json_metadata(metaData):
    try:
        if 'programDuration' in metaData['metadata']:
            return int(metaData['metadata']['programDuration']) / 60
        if 'duration' in metaData['metadata']:
            return int(metaData['metadata']['duration']) / 60
        return 0
    except:
        return 0

#Get program duration from json metadata
def programdurationstring_from_json_metadata(metaData, incBracketMin=True, incShortMin=False, incFullMin=False):
    try:
        durationInt = programdurationint_from_json_metadata(metaData)
        durationString = func.number_to_single_string(durationInt)
        if incBracketMin:
            return '(' + durationString + 'min)'
        elif incShortMin:
            return durationString + 'min'
        elif incFullMin:
            if durationString == '1':
                return durationString + ' minuut'
            else:
                return durationString + ' minuten'
        else:
            return durationString
    except:
        return ''

#Get program season from json metadata
def programseason_from_json_metadata(metaData, incBrackets=True):
    try:
        if incBrackets:
            return '(S' + str(metaData['metadata']['season']) + ')'
        else:
            return str(metaData['metadata']['season'])
    except:
        return ''

#Get program year from json metadata
def programyear_from_json_metadata(metaData):
    try:
        ProgramYear = str(metaData['metadata']['year'])
        if ProgramYear != '0':
            return '(' + ProgramYear + ')'
        return ''
    except:
        return ''

#Get program starrating from json metadata
def programstarrating_from_json_metadata(metaData):
    try:
        ProgramRating = str(metaData['metadata']['starRating'])
        if ProgramRating != '0' and ProgramRating != 'None':
            starCharacter = u'\u2605'
            return '(' + starCharacter + ProgramRating + ')'
        return ''
    except:
        return ''

#Get program agerating age from json metadata
def programagerating_from_json_metadata(metaData):
    try:
        ProgramRating = str(metaData['metadata']['pcLevel'])
        if ProgramRating != '99':
            return '(' + ProgramRating + '+)'
        return ''
    except:
        return ''

#Get program genres from json metadata
def programgenres_from_json_metadata(metaData):
    try:
        genresArray = metaData["metadata"]["genres"]
        ProgramGenres = ', '.join(filter(None, genresArray))
        if ProgramGenres == 'Overig':
            ProgramGenres = ''
        return ProgramGenres
    except:
        return ''

#Get program actors from json metadata
def programactors_from_json_metadata(metaData):
    try:
        actorsArray = metaData["metadata"]["actors"]
        if actorsArray != None:
            return ', '.join(filter(None, actorsArray))
        else:
            return ''
    except:
        return ''

#Get program presenters from json metadata
def programpresenters_from_json_metadata(metaData):
    try:
        presentersArray = metaData["metadata"]["presenters"]
        if presentersArray != None:
            return ', '.join(filter(None, presentersArray))
        else:
            return ''
    except:
        return ''

#Get program directors from json metadata
def programdirectors_from_json_metadata(metaData):
    try:
        directorsArray = metaData["metadata"]["directors"]
        if directorsArray != None:
            return ', '.join(filter(None, directorsArray))
        else:
            return ''
    except:
        return ''

#Get program description from json metadata
def programdescription_from_json_metadata(metaData):
    try:
        #Load long program description
        longDescription = hybrid.htmlparser_unescape(metaData["metadata"]["longDescription"])
        longDescription = hybrid.unicode_to_string(longDescription)
        longDescription = hybrid.htmlparser_unescape(longDescription)

        #Check program description
        if func.string_isnullorempty(longDescription) == False:
            return str(longDescription)
    except:
        pass

    try:
        #Load short program description
        shortDescription = hybrid.htmlparser_unescape(metaData["metadata"]["shortDescription"])
        shortDescription = hybrid.unicode_to_string(shortDescription)
        shortDescription = hybrid.htmlparser_unescape(shortDescription)

        #Check program description
        if func.string_isnullorempty(shortDescription) == False:
            return str(shortDescription)
    except:
        pass

    return 'Programmabeschrijving is niet geladen of beschikbaar.'

#Check if program is pay to play
def program_check_paytoplay(technicalPackageIds):
    try:
        technicalPackageIdsInt = technicalPackageIds.astype(int)
        if 101 and 10078 in technicalPackageIdsInt:
            return False
        return True
    except:
        return False

#Get episode title from json metadata
def episodetitle_from_json_metadata(metaData, returnEmpty=False):
    try:
        #Get the episode title
        if 'episodeTitle' in metaData['metadata']:
            EpisodeTitle = metaData['metadata']['episodeTitle']
        elif 'title' in metaData['metadata']:
            EpisodeTitle = metaData['metadata']['title']

        #Check empty episode title
        if func.string_isnullorempty(EpisodeTitle):
            if returnEmpty:
                return ''
            else:
                return 'Titel onbekend'

        return str(EpisodeTitle)
    except:
        if returnEmpty:
            return ''
        else:
            return 'Titel onbekend'

#Get episode number from json metadata
def episodenumber_from_json_metadata(metaData, incBrackets=True):
    try:
        if incBrackets:
            return '(A' + str(metaData['metadata']['episodeNumber']) + ')'
        else:
            return str(metaData['metadata']['episodeNumber'])
    except:
        return ''

#Check if content is for adults
def isAdult_from_json_metadata(metaData):
    try:
        if 'isAdult' in metaData['metadata']:
            return bool(metaData['metadata']['isAdult'])
        if 'isAdult' in metaData['channel']:
            return bool(metaData['channel']['isAdult'])
        return False
    except:
        return False

#Get stream asset id from json metadata
def stream_assetid_from_json_metadata(assetsArray):
    try:
        for asset in assetsArray:
            try:
                if asset['videoType'] == 'SD_DASH_WV':
                    if 'rights' in asset and asset['rights'] != 'watch': continue
                    return str(asset['assetId'])
            except:
                continue
        return ''
    except:
        return ''

#Get stream target bitrate
def get_stream_targetbitrate():
    try:
        streamResolutionSetting = var.addon.getSetting('StreamResolution')
        if streamResolutionSetting == '2160p' or streamResolutionSetting == '1080pBest':
            return '100000000'
        elif streamResolutionSetting == '1080pHigh':
            return '8000000'
        elif streamResolutionSetting == '1080p' or streamResolutionSetting == '1080pNormal':
            return '6000000'
        elif streamResolutionSetting == '720p':
            return '4000000'
        elif streamResolutionSetting == '576p':
            return '2500000'
        elif streamResolutionSetting == '432p':
            return '1600000'
        elif streamResolutionSetting == '360p':
            return '1200000'
        elif streamResolutionSetting == '180p':
            return '800000'
    except:
        pass
    return '100000000'

#Get stream target profile
def get_stream_targetprofile(playReadyStream=False):
    if playReadyStream:
        return 'M03'
    else:
        return 'G03'

#Get recording available time
def recording_available_time(metaData):
    ProgramAvailability = 'Onbekende beschikbaarheid'
    try:
        ProgramEndDateTime = programenddatetime_generate_from_json_metadata(metaData)
        DateTimeExpireEnd = ProgramEndDateTime + timedelta(days=func.days_in_year())
        DateTimeExpireMidnight = func.datetime_to_midnight(DateTimeExpireEnd)
        TimeRemainingSeconds = int((DateTimeExpireMidnight - datetime.now()).total_seconds())
        if TimeRemainingSeconds > 0:
            TimeRemainingDays = TimeRemainingSeconds // 86400
            TimeRemainingHours = (TimeRemainingSeconds - TimeRemainingDays * 86400) // 3600
            TimeRemainingMinutes = (TimeRemainingSeconds - TimeRemainingDays * 86400 - TimeRemainingHours * 3600) // 60
        else:
            return 'Programma niet meer beschikbaar'

        if TimeRemainingDays > 0:
            if TimeRemainingDays == 1:
                ProgramAvailability = 'Nog ' + str(TimeRemainingDays) + ' dag beschikbaar'
            else:
                ProgramAvailability = 'Nog ' + str(TimeRemainingDays) + ' dagen beschikbaar'
        elif TimeRemainingHours > 0:
            ProgramAvailability = 'Nog ' + str(TimeRemainingHours) + ' uur beschikbaar'
        elif TimeRemainingMinutes > 0:
            if TimeRemainingMinutes == 1:
                ProgramAvailability = 'Nog ' + str(TimeRemainingMinutes) + ' minuut beschikbaar'
            else:
                ProgramAvailability = 'Nog ' + str(TimeRemainingMinutes) + ' minuten beschikbaar'
        elif TimeRemainingSeconds > 0:
            ProgramAvailability = 'Nog ' + str(TimeRemainingSeconds) + ' seconden beschikbaar'
        return ProgramAvailability
    except:
        return ProgramAvailability

#Get vod week available time
def vod_week_available_time(metaData):
    ProgramAvailability = 'Onbekende beschikbaarheid'
    try:
        DateTimeStartTime = programstartdatetime_from_json_metadata(metaData)
        DateTimeExpireTime = DateTimeStartTime + timedelta(days=var.VodDaysOffsetPast)
        TimeRemainingSeconds = int((DateTimeExpireTime - datetime.now()).total_seconds())
        if TimeRemainingSeconds > 0:
            TimeRemainingDays = TimeRemainingSeconds // 86400
            TimeRemainingHours = (TimeRemainingSeconds - TimeRemainingDays * 86400) // 3600
            TimeRemainingMinutes = (TimeRemainingSeconds - TimeRemainingDays * 86400 - TimeRemainingHours * 3600) // 60
        else:
            return 'Programma niet meer beschikbaar'

        if TimeRemainingDays > 0:
            if TimeRemainingDays == 1:
                ProgramAvailability = 'Nog ' + str(TimeRemainingDays) + ' dag beschikbaar'
            else:
                ProgramAvailability = 'Nog ' + str(TimeRemainingDays) + ' dagen beschikbaar'
        elif TimeRemainingHours > 0:
            ProgramAvailability = 'Nog ' + str(TimeRemainingHours) + ' uur beschikbaar'
        elif TimeRemainingMinutes > 0:
            if TimeRemainingMinutes == 1:
                ProgramAvailability = 'Nog ' + str(TimeRemainingMinutes) + ' minuut beschikbaar'
            else:
                ProgramAvailability = 'Nog ' + str(TimeRemainingMinutes) + ' minuten beschikbaar'
        elif TimeRemainingSeconds > 0:
            ProgramAvailability = 'Nog ' + str(TimeRemainingSeconds) + ' seconden beschikbaar'
        return ProgramAvailability
    except:
        return ProgramAvailability

#Get vod ondemand available time
def vod_ondemand_available_time(metaData):
    ProgramAvailability = 'Onbekende beschikbaarheid'
    try:
        DateTimeExpireTime = contractenddatetime_from_json_metadata(metaData)
        TimeRemainingSeconds = int((DateTimeExpireTime - datetime.now()).total_seconds())
        if TimeRemainingSeconds > 0:
            TimeRemainingDays = TimeRemainingSeconds // 86400
            TimeRemainingHours = (TimeRemainingSeconds - TimeRemainingDays * 86400) // 3600
            TimeRemainingMinutes = (TimeRemainingSeconds - TimeRemainingDays * 86400 - TimeRemainingHours * 3600) // 60
        else:
            return 'Programma niet meer beschikbaar'

        if TimeRemainingDays > 0:
            if TimeRemainingDays == 1:
                ProgramAvailability = 'Nog ' + str(TimeRemainingDays) + ' dag beschikbaar'
            else:
                ProgramAvailability = 'Nog ' + str(TimeRemainingDays) + ' dagen beschikbaar'
        elif TimeRemainingHours > 0:
            ProgramAvailability = 'Nog ' + str(TimeRemainingHours) + ' uur beschikbaar'
        elif TimeRemainingMinutes > 0:
            if TimeRemainingMinutes == 1:
                ProgramAvailability = 'Nog ' + str(TimeRemainingMinutes) + ' minuut beschikbaar'
            else:
                ProgramAvailability = 'Nog ' + str(TimeRemainingMinutes) + ' minuten beschikbaar'
        elif TimeRemainingSeconds > 0:
            ProgramAvailability = 'Nog ' + str(TimeRemainingSeconds) + ' seconden beschikbaar'
        return ProgramAvailability
    except:
        return ProgramAvailability