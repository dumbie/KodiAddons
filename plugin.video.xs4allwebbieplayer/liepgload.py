from datetime import datetime, timedelta
import func
import metadatainfo
import metadatacombine
import xbmcgui
import path
import var

def list_load(listContainer, epgJson):
    for program in epgJson['containers']:
        try:
            #Set the current player play time
            dateTimeNow = datetime.now()

            #Load program basics
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeStartDateTime = func.datetime_remove_seconds(ProgramTimeStartDateTime)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(program)

            #Check if program is starting or ending on target day
            if ProgramTimeStartDateTime.date() != var.EpgCurrentLoadDateTime.date() and ProgramTimeEndDateTime.date() != var.EpgCurrentLoadDateTime.date():
                continue

            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if var.SearchFilterTerm != '':
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchFilterTerm in searchMatch
                if searchResultFound == False:
                    continue

            #Load program details
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))
            ProgramDurationString = metadatainfo.programdurationstring_from_json_metadata(program, False, False, True)
            ProgramDescription = 'Programmabeschrijving wordt geladen.'
            ProgramEpgList = 'Programmaduur wordt geladen'

            #Combine program description extended
            ProgramDescriptionRaw = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Check if program vod is available for playback
            contentOptionsArray = metadatainfo.contentOptions_from_json_metadata(program)
            if 'CATCHUP' in contentOptionsArray:
                ProgramIsAvailable = 'true'
            else:
                ProgramIsAvailable = 'false'

            #Check if the program is part of series
            ProgramRecordSeriesId = metadatainfo.seriesId_from_json_metadata(program)

            #Check if current program is a rerun
            programRerunName = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramName.lower())
            programRerunDescription = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramDescription.lower())
            if programRerunName or programRerunDescription:
                ProgramRerun = 'true'
            else:
                ProgramRerun = 'false'

            #Add program to the list container
            listItem = xbmcgui.ListItem()
            listItem.setProperty('AssetId', var.EpgCurrentAssetId)
            listItem.setProperty('ChannelId', var.EpgCurrentChannelId)
            listItem.setProperty('ExternalId', var.EpgCurrentExternalId)
            listItem.setProperty('ChannelName', var.EpgCurrentChannelName)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramRerun', ProgramRerun)
            listItem.setProperty('ProgramDuration', ProgramDurationString)
            listItem.setProperty('ProgramRecordSeriesId', ProgramRecordSeriesId)
            listItem.setProperty('ProgramDescriptionRaw', ProgramDescriptionRaw)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setProperty('ProgramEpgList', ProgramEpgList)
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty('ProgramTimeStart', str(ProgramTimeStartDateTime))
            listItem.setProperty('ProgramTimeEnd', str(ProgramTimeEndDateTime))
            listItem.setInfo('video', {'Genre': 'TV Gids', 'Plot': ProgramDescriptionRaw})
            listItem.setArt({'thumb': path.icon_television(var.EpgCurrentExternalId), 'icon': path.icon_television(var.EpgCurrentExternalId)})

            #Check if program finished airing
            if ProgramProgressPercent >= 100:
                listItem.setProperty('ProgramIsAvailable', ProgramIsAvailable)

            #Check if program is still airing
            if ProgramProgressPercent > 0 and ProgramProgressPercent < 100:
                listItem.setProperty('ProgramIsAiring', 'true')

            #Add generated listitem
            listContainer.addItem(listItem)
        except:
            continue
