from datetime import datetime, timedelta
import func
import metadatainfo

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
                ProgramListString += '\n' + ProgramListTimeStartString + ' ' + ProgramListTimeDurationString + ' [COLOR gray]' + ProgramListName + '[/COLOR]'
                ProgramListId += 1
            except:
                break

        if func.string_isnullorempty(ProgramListString) == True:
            return ''
        else:
            return '[COLOR gray]Later op deze zender[/COLOR]' + ProgramListString
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
                ProgramListString += '\n' + ProgramListTimeStartString + ' ' + ProgramListTimeDurationString + ' [COLOR gray]' + ProgramListName + '[/COLOR]'
                ProgramListId += 1
            except:
                break

        if func.string_isnullorempty(ProgramListString) == True:
            return ''
        else:
            return '[COLOR gray]Eerder op deze zender[/COLOR]' + ProgramListString
    except:
        return ''

def program_timing_vod(metaData):
    try:
        ProgramDuration = metadatainfo.programdurationstring_from_json_metadata(metaData, False, False, True)
        ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
        ProgramTimeStartStringTime = ProgramTimeStartDateTime.strftime('%H:%M')
        ProgramTimeStartStringDate = ProgramTimeStartDateTime.strftime('%a, %d %B %Y')
        return '[COLOR gray]Begon om[/COLOR] ' + ProgramTimeStartStringTime + ' [COLOR gray]op[/COLOR] ' + ProgramTimeStartStringDate + ' [COLOR gray]en duurde[/COLOR] ' + ProgramDuration
    except:
        return ''

def program_timing_program_metadata(metaData, dateTimeNow, dateTimeSeek):
    try:
        ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(metaData)
        ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
        ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
        ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(metaData)
        ProgramTimeDurationString = metadatainfo.programdurationstring_from_json_metadata(metaData, False, False, True)
        ProgramTimeLeftMinutes = int((ProgramTimeEndDateTime - dateTimeSeek).total_seconds() / 60)
        ProgramTimeLeftString = str(ProgramTimeLeftMinutes)
        ProgramTimeEndString = (dateTimeNow + timedelta(minutes=ProgramTimeLeftMinutes)).strftime('%H:%M')

        if ProgramTimeDurationString == '0':
            return '[COLOR gray]onbekend programmaduur[/COLOR]'
        elif ProgramTimeLeftString == '0':
            return '[COLOR gray]is bijna afgelopen, duurde[/COLOR] ' + ProgramTimeDurationString + '[COLOR gray], begon om[/COLOR] ' + ProgramTimeStartString
        else:
            return '[COLOR gray]duurt nog[/COLOR] ' + ProgramTimeLeftString + ' [COLOR gray]van de[/COLOR] ' + ProgramTimeDurationString + '[COLOR gray], begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR gray]eindigt rond[/COLOR] ' + ProgramTimeEndString
    except:
        return ''

def program_timing_program_property(propertyData, dateTimeNow, returnShort=False):
    try:
        ProgramTimeStartProp = propertyData.getProperty('ProgramTimeStart')
        ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStartProp, '%Y-%m-%d %H:%M:%S')
        ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
        ProgramTimeStartString = ProgramTimeStartDateTime.strftime('%H:%M')
        ProgramTimeEndProp = propertyData.getProperty('ProgramTimeEnd')
        ProgramTimeEndDateTime = func.datetime_from_string(ProgramTimeEndProp, '%Y-%m-%d %H:%M:%S')
        ProgramTimeDurationString = propertyData.getProperty('ProgramDuration')
        ProgramTimeLeftMinutes = int((ProgramTimeEndDateTime - dateTimeNow).total_seconds() / 60)
        ProgramTimeLeftString = str(ProgramTimeLeftMinutes)
        ProgramTimeEndString = ProgramTimeEndDateTime.strftime('%H:%M')

        if ProgramTimeDurationString == '0':
            if returnShort == True:
                return 'onbekend programmaduur'
            else:
                return '[COLOR gray]onbekend programmaduur[/COLOR]'
        if func.date_time_between(dateTimeNow, ProgramTimeStartDateTime, ProgramTimeEndDateTime):
            if ProgramTimeLeftString == '0':
                if returnShort == True:
                    return 'is bijna afgelopen, duurde ' + ProgramTimeDurationString
                else:
                    return '[COLOR gray]is bijna afgelopen, duurde[/COLOR] ' + ProgramTimeDurationString + '[COLOR gray], begon om[/COLOR] ' + ProgramTimeStartString
            else:
                if returnShort == True:
                    return 'duurt nog ' + ProgramTimeLeftString + ' van de ' + ProgramTimeDurationString
                else:
                    return '[COLOR gray]duurt nog[/COLOR] ' + ProgramTimeLeftString + ' [COLOR gray]van de[/COLOR] ' + ProgramTimeDurationString + '[COLOR gray], begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR gray]eindigt rond[/COLOR] ' + ProgramTimeEndString
        elif dateTimeNow > ProgramTimeEndDateTime:
            if returnShort == True:
                return 'duurde ' + ProgramTimeDurationString
            else:
                return '[COLOR gray]duurde[/COLOR] ' + ProgramTimeDurationString + '[COLOR gray], begon om[/COLOR] ' + ProgramTimeStartString + ' [COLOR gray]eindigde rond[/COLOR] ' + ProgramTimeEndString
        else:
            if returnShort == True:
                return 'duurt ' + ProgramTimeDurationString
            else:
                return '[COLOR gray]duurt[/COLOR] ' + ProgramTimeDurationString + '[COLOR gray], begint om[/COLOR] ' + ProgramTimeStartString + ' [COLOR gray]eindigt rond[/COLOR] ' + ProgramTimeEndString
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
            programGenres = 'Genres [COLOR gray]' + programGenres + '[/COLOR]'
        return programGenres
    except:
        return ''

def program_actors_directors(metaData):
    try:
        #Load program actors
        programActors = metadatainfo.programactors_from_json_metadata(metaData)

        #Load program directors
        programDirectors = metadatainfo.programdirectors_from_json_metadata(metaData)

        #Check if directors string is empty
        actorsNull = func.string_isnullorempty(programActors)
        directorsNull = func.string_isnullorempty(programDirectors)

        if actorsNull == True and directorsNull == True:
                return ''
        elif actorsNull == True and directorsNull == False:
            return 'Regie [COLOR gray]' + programDirectors + '[/COLOR]'
        elif actorsNull == False and directorsNull == True:
            return 'Acteurs [COLOR gray]' + programActors + '[/COLOR]'
        else:
            return 'Regie [COLOR gray]' + programDirectors + '[/COLOR] Acteurs [COLOR gray]' + programActors + '[/COLOR]'
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
            ProgramDetails = '[COLOR gray]' + ProgramEpisodeTitle + '[/COLOR] ' + ProgramDetails
        else:
            ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'

        #Return program details
        return ProgramDetails
    except:
        return ''
