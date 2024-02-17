from datetime import datetime, timedelta
import download
import func
import lifunc
import metadatafunc
import metadatainfo
import metadatacombine
import xbmcgui
import path
import var

def list_load_combined(listContainer, forceUpdate=False):
    try:
        #Download epg day
        var.EpgCurrentDayDataJson = download.download_epg_day(var.EpgCurrentLoadDateTime, forceUpdate)
        if var.EpgCurrentDayDataJson == None:
            notificationIcon = path.resources('resources/skins/default/media/common/epg.png')
            xbmcgui.Dialog().notification(var.addonname, "Tv Gids downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        if func.string_isnullorempty(var.SearchTermCurrent):
            #Load programs for current channel on set day
            channelEpgJson = metadatafunc.search_channelid_jsonepg(var.EpgCurrentDayDataJson, var.EpgCurrentChannelId)
            if channelEpgJson != None:
                list_load_append(listContainerSort, channelEpgJson)
        else:
            #Load programs for search term from all channels on set day
            for channelEpgJson in var.EpgCurrentDayDataJson["resultObj"]["containers"]:
                list_load_append(listContainerSort, channelEpgJson)

        #Sort list items
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramTimeStart'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, epgJson):
    #Set the current player play time
    dateTimeNow = datetime.now()

    for program in epgJson['containers']:
        try:
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
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False:
                    continue

            #Load channel basics
            ChannelId = metadatainfo.channelId_from_json_metadata(program)
            ChannelExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ChannelName = metadatainfo.channelName_from_json_metadata(program)
            ChannelIsAdult = metadatainfo.isAdult_from_json_metadata(program)

            #Check if channel is filtered
            if func.setting_get('TelevisionChannelNoErotic') == 'true' and ChannelIsAdult == True: continue

            #Load program details
            ProgramId = metadatainfo.contentId_from_json_metadata(program)
            ProgramProgressPercent = int(((dateTimeNow - ProgramTimeStartDateTime).total_seconds() / 60) * 100 / ((ProgramTimeEndDateTime - ProgramTimeStartDateTime).total_seconds() / 60))
            ProgramDurationString = metadatainfo.programdurationstring_from_json_metadata(program, False, False, True)
            ProgramDescriptionDesc = 'Programmabeschrijving wordt geladen.'
            ProgramEpgList = 'Programmaduur wordt geladen'

            #Combine program description extended
            ProgramDescriptionRaw = metadatacombine.program_description_extended(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, True, True)

            #Check if the program is part of series
            ProgramRecordSeriesId = metadatainfo.seriesId_from_json_metadata(program)

            #Check if current program is a rerun
            programRerunName = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramName.lower())
            programRerunDescription = any(substring for substring in var.ProgramRerunSearchTerm if substring in ProgramDescriptionRaw.lower())
            if programRerunName or programRerunDescription:
                ProgramRerun = 'true'
            else:
                ProgramRerun = 'false'

            #Check if program vod playback is allowed
            contentOptionsArray = metadatainfo.contentOptions_from_json_metadata(program)
            if 'CATCHUP' in contentOptionsArray:
                ProgramIsCatchup = 'true'
            else:
                ProgramIsCatchup = 'false'

            #Set item icons
            iconDefault = path.icon_television(ChannelExternalId)

            #Set item details
            listItem = xbmcgui.ListItem()
            listItem.setProperty('ExternalId', ChannelExternalId)
            listItem.setProperty('ChannelId', ChannelId)
            listItem.setProperty('ChannelName', ChannelName)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramRerun', ProgramRerun)
            listItem.setProperty('ProgramIsCatchup', ProgramIsCatchup)
            listItem.setProperty('ProgramDuration', ProgramDurationString)
            listItem.setProperty('ProgramRecordSeriesId', ProgramRecordSeriesId)
            listItem.setProperty('ProgramDescriptionRaw', ProgramDescriptionRaw)
            listItem.setProperty('ProgramDescriptionDesc', ProgramDescriptionDesc)
            listItem.setProperty('ProgramEpgList', ProgramEpgList)
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setProperty('ProgramTimeStart', str(ProgramTimeStartDateTime))
            listItem.setProperty('ProgramTimeEnd', str(ProgramTimeEndDateTime))
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDescriptionRaw})
            listItem.setArt({'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault})

            #Check if program finished airing
            if ProgramProgressPercent >= 100:
                listItem.setProperty('ProgramIsAvailable', ProgramIsCatchup)

            #Check if program is still to come
            if ProgramProgressPercent <= 0:
                listItem.setProperty('ProgramIsUpcoming', 'true')

            #Check if program is currently airing
            if ProgramProgressPercent > 0 and ProgramProgressPercent < 100:
                listItem.setProperty('ProgramIsAiring', 'true')

            #Add generated listitem
            listContainer.append(listItem)
        except:
            continue
