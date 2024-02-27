import xbmcgui
import download
import lifunc
import metadatacombine
import metadatainfo
import path
import recordingfunc
import var

def list_load_combined(listContainer=None, forceUpdate=False):
    try:
        #Download record events
        downloadResult = download.download_recording_event(forceUpdate)
        if downloadResult == False:
            notificationIcon = path.resources('resources/skins/default/media/common/record.png')
            xbmcgui.Dialog().notification(var.addonname, "Geplande opnames downloaden mislukt.", notificationIcon, 2500, False)
            return False

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Sort list items
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramTimeStart'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    for program in var.RecordingEventDataJson["resultObj"]["containers"]:
        try:
            #Load and check recording status
            if recordingfunc.check_status_scheduled(program) == False:
                continue

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramDeltaTimeStart = str(metadatainfo.programstartdeltatime_from_json_metadata(program))
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)
            ProgramDescription = 'Van ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' tot ' + ProgramTimeEndDateTime.strftime('%H:%M') + ' op ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, False, False)

            #Update program name string
            ProgramName += ' ' + ProgramDetails

            #Set item icons
            iconDefault = path.icon_television(ExternalId)

            #Set item details
            listItem = xbmcgui.ListItem()
            listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
            listItem.setProperty('ProgramTimeStart', str(ProgramTimeStartDateTime))
            listItem.setProperty('ProgramDeltaTimeStart', ProgramDeltaTimeStart)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setArt({'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault})
            listContainer.append(listItem)
        except:
            continue
