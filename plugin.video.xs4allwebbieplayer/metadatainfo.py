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
        channelNameString = metaData['metadata']['channelName']
        channelNameString = hybrid.unicode_to_string(channelNameString)
        channelNameString = hybrid.htmlparser_unescape(channelNameString)

        #Check the channel name
        if func.string_isnullorempty(channelNameString):
            channelNameString = "Onbekende zender"

        return channelNameString
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
        if 'externalChannelId' in metaData['channel']:
            return str(metaData['channel']['externalChannelId'])
        if 'externalChannelId' in metaData['metadata']:
            return str(metaData['metadata']['externalChannelId'])
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

        return programNameString
    except:
        return 'Onbekend programma'

#Get program startdelta from json metadata
def programstartdeltatime_from_json_metadata(metaData):
    try:
        return int(metaData['metadata']['startDeltaTime'])
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
def programdurationstring_from_json_metadata(metaData, incBrackets=True, incMin=True):
    try:
        durationInt = programdurationint_from_json_metadata(metaData)
        if incBrackets:
            return '(' + func.number_to_single_string(durationInt) + 'min)'
        elif incMin:
            return func.number_to_single_string(durationInt) + 'min'
        else:
            return func.number_to_single_string(durationInt)
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
        if ProgramRating != '0':
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

#Get program description from json metadata
def programdescription_from_json_metadata(metaData):
    #Check the long program description
    try:
        return hybrid.htmlparser_unescape(metaData["metadata"]["longDescription"])
    except:
        pass

    #Check the short program description
    try:
        return hybrid.htmlparser_unescape(metaData["metadata"]["shortDescription"])
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
def episodetitle_from_json_metadata(metaData, returnEmpty=False, programTitle=''):
    try:
        #Get the episode title
        if 'episodeTitle' in metaData['metadata']:
            EpisodeTitle = metaData['metadata']['episodeTitle']
        elif 'title' in metaData['metadata']:
            EpisodeTitle = metaData['metadata']['title']

        #Check same episode title
        if EpisodeTitle == programTitle:
            if returnEmpty:
                return ''
            else:
                return 'Titelloos'

        #Check empty episode title
        if func.string_isnullorempty(EpisodeTitle):
            if returnEmpty:
                return ''
            else:
                return 'Titel onbekend'

        return EpisodeTitle
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
        return bool(metaData["metadata"]["isAdult"])
    except:
        return False

#Get dash widevine stream asset id
def get_stream_assetid(assetsArray):
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
            return ProgramAvailability

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
            return ProgramAvailability

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
            return ProgramAvailability

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