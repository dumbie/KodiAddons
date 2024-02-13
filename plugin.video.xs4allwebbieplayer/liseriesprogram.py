import download
import func
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
import var

def list_load_combined(listContainer=None, forceUpdate=False):
    try:
        #Download programs
        downloadResultVod = download.download_vod_series(forceUpdate)
        downloadResultProgram = download.download_search_series(forceUpdate)
        if downloadResultVod == False or downloadResultProgram == False:
            notificationIcon = path.resources('resources/skins/default/media/common/series.png')
            xbmcgui.Dialog().notification(var.addonname, "Series downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_program_append(listContainerSort)
        list_load_vod_append(listContainerSort)

        #Sort items in list
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramName'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_vod_append(listContainer):
    for program in var.SeriesVodDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Load program details
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Add vod program
            listAction = 'load_series_episodes_vod'
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('PictureUrl', PictureUrl)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails})
            iconStreamType = path.icon_addon('vod')
            iconProgram = path.icon_vod(PictureUrl)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType})
            dirIsfolder = True
            dirUrl = var.LaunchUrl + '?' + listAction + '=' + ProgramId + var.splitchar + ProgramName + var.splitchar + PictureUrl
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue

def list_load_program_append(listContainer):
    for program in var.SeriesProgramDataJson['resultObj']['containers']:
        try:
            #Load program basics
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)

            #Check if serie is already added
            tupleContainer = [x[1] for x in listContainer]
            if lifunc.search_programname_listarray(tupleContainer, ProgramName) != None: continue

            #Check if there are search results
            if func.string_isnullorempty(var.SearchTermCurrent) == False:
                searchMatch = func.search_filter_string(ProgramName)
                searchResultFound = var.SearchTermCurrent in searchMatch
                if searchResultFound == False: continue

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            PictureUrl = metadatainfo.pictureUrl_from_json_metadata(program)
            SeriesId = metadatainfo.seriesId_from_json_metadata(program)
            ProgramId = metadatainfo.contentId_from_json_metadata(program)

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, False, False, False, True)

            #Add week program
            listAction = 'load_series_episodes_program'
            listItem = xbmcgui.ListItem(ProgramName)
            listItem.setProperty('Action', listAction)
            listItem.setProperty('PictureUrl', PictureUrl)
            listItem.setProperty('SeriesId', SeriesId)
            listItem.setProperty('ProgramId', ProgramId)
            listItem.setProperty("ProgramName", ProgramName)
            listItem.setProperty("ProgramWeek", 'true')
            listItem.setProperty('ProgramDetails', ProgramDetails)
            listItem.setInfo('video', {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Plot': ProgramDetails})
            iconStreamType = path.icon_addon('calendarweek')
            iconProgram = path.icon_epg(PictureUrl)
            iconChannel = path.icon_television(ExternalId)
            listItem.setArt({'thumb': iconProgram, 'icon': iconProgram, 'image1': iconStreamType, 'image2': iconChannel})
            dirIsfolder = True
            dirUrl = var.LaunchUrl + '?' + listAction + '=' + ProgramId + var.splitchar + ProgramName + var.splitchar + PictureUrl
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
