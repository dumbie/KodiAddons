from datetime import datetime, timedelta
import metadatainfo
import func

def program_upcoming_list(metaData, programIndex):
    try:
        ProgramListId = 1
        ProgramListString = ''
        while ProgramListId < 5:
            try:
                ProgramListMetaData = metaData[programIndex + ProgramListId]
                ProgramListName = metadatainfo.programtitle_from_json_metadata(ProgramListMetaData)
                ProgramListTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(ProgramListMetaData)
                ProgramListTimeStartString = ProgramListTimeStartDateTime.strftime('%H:%M')
                ProgramListTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(ProgramListMetaData)
                ProgramListString += '\n' + ProgramListTimeStartString + ' ' + ProgramListTimeDurationString + ' [COLOR FF888888]' + ProgramListName + '[/COLOR]'
                ProgramListId += 1
            except:
                break

        if func.string_isnullorempty(ProgramListString) == True:
            return ''
        else:
            return '[COLOR FF888888]Later op deze zender[/COLOR]' + ProgramListString
    except:
        return ''

def program_earlier_list(metaData, programIndex):
    try:
        ProgramListId = 1
        ProgramListString = ''
        while ProgramListId < 5:
            try:
                ProgramListMetaData = metaData[programIndex - ProgramListId]
                ProgramListName = metadatainfo.programtitle_from_json_metadata(ProgramListMetaData)
                ProgramListTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(ProgramListMetaData)
                ProgramListTimeStartString = ProgramListTimeStartDateTime.strftime('%H:%M')
                ProgramListTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(ProgramListMetaData)
                ProgramListString += '\n' + ProgramListTimeStartString + ' ' + ProgramListTimeDurationString + ' [COLOR FF888888]' + ProgramListName + '[/COLOR]'
                ProgramListId += 1
            except:
                break

        if func.string_isnullorempty(ProgramListString) == True:
            return ''
        else:
            return '[COLOR FF888888]Eerder op deze zender[/COLOR]' + ProgramListString
    except:
        return ''

def program_timing_vod(metaData):
    try:
        ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(metaData, False, False, True)
        ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramTimeStartStringTime = ProgramTimeStartDateTime.strftime('%H:%M')
        ProgramTimeStartStringDate = ProgramTimeStartDateTime.strftime('%a, %d %B %Y')
        return '[COLOR FF888888]Begon om[/COLOR] ' + ProgramTimeStartStringTime + ' [COLOR FF888888]op[/COLOR] ' + ProgramTimeStartStringDate + ' [COLOR FF888888]en duurde[/COLOR] ' + ProgramDuration
    except:
        return ''

def program_timing_program_metadata(metaData, dateTimeNow, dateTimeSeek):
    try:
        ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
        ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(metaData)
        ProgramTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False, False, True)
        ProgramTimeLeftMinutes = int((ProgramTimeEndDateTime - dateTimeSeek).total_seconds() / 60)
        ProgramTimeLeftString = str(ProgramTimeLeftMinutes)
        ProgramTimeEndString = (dateTimeNow + timedelta(minutes=ProgramTimeLeftMinutes)).strftime('%H:%M')

        if ProgramTimeDurationString == '0':
            return '[COLOR FF888888]onbekend programmaduur[/COLOR]'
        elif ProgramTimeLeftString == '0':
            return '[COLOR FF888888]is bijna afgelopen, duurde[/COLOR] ' + ProgramTimeDurationString + '[COLOR FF888888], begon om[/COLOR] ' + ProgramTimeStartString
        else:
            return '[COLOR FF888888]duurt nog[/COLOR] ' + ProgramTimeLeftString + ' [COLOR FF888888]van de[/COLOR] ' + ProgramTimeDurationString + '[COLOR FF888888], begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR FF888888]eindigt rond[/COLOR] ' + ProgramTimeEndString
    except:
        return ''

def program_timing_program_property(propertyData, dateTimeNow, returnShort=False):
    try:
        ProgramTimeStart = propertyData.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStart, '%Y-%m-%d %H:%M:%S')
        ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
        ProgramTimeEnd = propertyData.getProperty('ProgramTimeEnd')
        ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEnd, '%Y-%m-%d %H:%M:%S')
        ProgramTimeDurationString = propertyData.getProperty('ProgramDuration')
        ProgramTimeLeftMinutes = int((ProgramTimeEndDateTime - dateTimeNow).total_seconds() / 60)
        ProgramTimeLeftString = str(ProgramTimeLeftMinutes)
        ProgramTimeEndString = ProgramTimeEndDateTime.strftime('%H:%M')

        if ProgramTimeDurationString == '0':
            if returnShort == True:
                return '[COLOR FF888888]onbekend programmaduur[/COLOR]'
            else:
                return '[COLOR FF888888]onbekend programmaduur[/COLOR]'

        if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
            if ProgramTimeLeftString == '0':
                if returnShort == True:
                    return '[COLOR FF888888]is bijna afgelopen, duurde[/COLOR] ' + ProgramTimeDurationString
                else:
                    return '[COLOR FF888888]is bijna afgelopen, duurde[/COLOR] ' + ProgramTimeDurationString + '[COLOR FF888888], begon om[/COLOR] ' + ProgramTimeStartString
            else:
                if returnShort == True:
                    return '[COLOR FF888888]duurt nog[/COLOR] ' + ProgramTimeLeftString + ' [COLOR FF888888]van de[/COLOR] ' + ProgramTimeDurationString
                else:
                    return '[COLOR FF888888]duurt nog[/COLOR] ' + ProgramTimeLeftString + ' [COLOR FF888888]van de[/COLOR] ' + ProgramTimeDurationString + '[COLOR FF888888], begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR FF888888]eindigt rond[/COLOR] ' + ProgramTimeEndString
        elif dateTimeNow > ProgramTimeEndDateTime:
            if returnShort == True:
                return '[COLOR FF888888]duurde[/COLOR] ' + ProgramTimeDurationString
            else:
                return '[COLOR FF888888]duurde[/COLOR] ' + ProgramTimeDurationString + '[COLOR FF888888], begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR FF888888]eindigde rond[/COLOR] ' + ProgramTimeEndString
        else:
            if returnShort == True:
                return '[COLOR FF888888]duurt[/COLOR] ' + ProgramTimeDurationString
            else:
                return '[COLOR FF888888]duurt[/COLOR] ' + ProgramTimeDurationString + '[COLOR FF888888], begint om[/COLOR] ' + ProgramTimeStartString + ' [COLOR FF888888]eindigt rond[/COLOR] ' + ProgramTimeEndString
    except:
        return ''

def program_description_extended(metaData, addGenres=True, addActors=True):
    try:
        #Load program description
        ProgramDescription = metadatainfo.programdescription_from_json_metadata(metaData)

        #Load program genres
        if addGenres == True:
            ProgramGenres = program_genres(metaData)
        else:
            ProgramGenres = ''

        #Load program actors and directors
        if addActors == True:
            ProgramActors = program_actors_directors(metaData)
        else:
            ProgramActors = ''

        #Combine program genres
        if func.string_isnullorempty(ProgramGenres) == False:
            ProgramDescription += "\n\n" + ProgramGenres

        #Combine program actors
        if func.string_isnullorempty(ProgramActors) == False:
            ProgramDescription += "\n\n" + ProgramActors

        #Return description
        return ProgramDescription
    except:
        return ''

def program_genres(metaData):
    try:
        programGenres = metadatainfo.programgenres_from_json_metadata(metaData)
        if func.string_isnullorempty(programGenres) == False:
            programGenres = 'Genres [COLOR FF888888]' + programGenres + '[/COLOR]'
        return programGenres
    except:
        return ''

def program_actors_directors(metaData):
    try:
        #Load program directors
        programDirectors = metadatainfo.programdirectors_from_json_metadata(metaData)

        #Load program actors
        programActors = metadatainfo.programactors_from_json_metadata(metaData)

        #Load program presenters
        programPresenters = metadatainfo.programpresenters_from_json_metadata(metaData)

        #Check if string is empty
        directorsNull = func.string_isnullorempty(programDirectors)
        actorsNull = func.string_isnullorempty(programActors)
        presentersNull = func.string_isnullorempty(programPresenters)

        if actorsNull == True and directorsNull == True and presentersNull == True:
                return ''

        if directorsNull == False:
            programDirectors = 'Regie [COLOR FF888888]' + programDirectors + '[/COLOR]'

        if actorsNull == False:
            programActors = 'Acteurs [COLOR FF888888]' + programActors + '[/COLOR]'

        if presentersNull == False:
            programPresenters = 'Presentatoren [COLOR FF888888]' + programPresenters + '[/COLOR]'

        #Combine cast details
        stringJoin = [ programDirectors, programActors, programPresenters ]
        return ' '.join(filter(None, stringJoin))
    except:
        return ''

def program_details(metaData, returnShort=False, addDuration=False, addYear=False, addSeason=False, addEpisodeNumber=False, addEpisodeTitle=False, addRating=False):
    try:
        #Load program details
        if addDuration == True:
            ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(metaData)
        else:
            ProgramDuration = ''
        if addYear == True:
            ProgramYear = metadatainfo.programyear_from_json_metadata(metaData)
        else:
            ProgramYear = ''
        if addSeason == True:
            ProgramSeason = metadatainfo.programseason_from_json_metadata(metaData)
        else:
            ProgramSeason = ''
        if addEpisodeNumber == True:
            ProgramEpisodeNumber = metadatainfo.episodenumber_from_json_metadata(metaData)
        else:
            ProgramEpisodeNumber = ''
        if addEpisodeTitle == True:
            ProgramEpisodeTitle = metadatainfo.episodetitle_from_json_metadata(metaData, True)
        else:
            ProgramEpisodeTitle = ''
        if addRating == True:
            ProgramStarRating = metadatainfo.programstarrating_from_json_metadata(metaData)
            ProgramAgeRating = metadatainfo.programagerating_from_json_metadata(metaData)
        else:
            ProgramStarRating = ''
            ProgramAgeRating = ''

        #Combine program details
        stringJoin = [ ProgramDuration, ProgramYear, ProgramSeason, ProgramEpisodeNumber, ProgramStarRating, ProgramAgeRating ]
        ProgramDetails = ' '.join(filter(None, stringJoin))

        if func.string_isnullorempty(ProgramDetails) == True:
            if returnShort:
                ProgramDetails = '(?)'
            else:
                ProgramDetails = 'Onbekend seizoen en aflevering'

        #Add program episode title and color
        if func.string_isnullorempty(ProgramEpisodeTitle) == False:
            ProgramDetails = '[COLOR FF888888]' + ProgramEpisodeTitle + '[/COLOR] ' + ProgramDetails
        else:
            ProgramDetails = '[COLOR FF888888]' + ProgramDetails + '[/COLOR]'

        #Return program details
        return ProgramDetails
    except:
        return ''
