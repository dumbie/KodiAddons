import func
import metadatainfo

def program_description_extended(metaData, addGenres=True, addActors=True):
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

def program_genres(metaData):
    programGenres = metadatainfo.programgenres_from_json_metadata(metaData)
    if func.string_isnullorempty(programGenres) == False:
        programGenres = 'Genres: [COLOR gray]' + programGenres + '[/COLOR]'
    return programGenres

def program_actors_directors(metaData):
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
        return 'Regie: [COLOR gray]' + programDirectors + '[/COLOR]'
    elif actorsNull == False and directorsNull == True:
        return 'Acteurs: [COLOR gray]' + programActors + '[/COLOR]'
    else:
        return 'Regie: [COLOR gray]' + programDirectors + '[/COLOR] Acteurs: [COLOR gray]' + programActors + '[/COLOR]'

def program_details(metaData, returnShort=False, addDuration=False, addYear=False, addSeason=False, addEpisodeNumber=False, addEpisodeTitle=False, addRating=False):
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

    ProgramDetails = '[COLOR gray]' + ProgramDetails + '[/COLOR]'

    if func.string_isnullorempty(ProgramEpisodeTitle) == False:
        ProgramDetails = ProgramEpisodeTitle + " " + ProgramDetails

    #Return program details
    return ProgramDetails
