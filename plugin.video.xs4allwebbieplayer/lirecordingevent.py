import xbmcgui
import dlrecordingevent
import lifunc
import metadatacombine
import metadatainfo
import path
import recordingfunc
import var

def list_load_combined(listContainer=None):
    try:
        #Download record events
        downloadResult = dlrecordingevent.download()
        if downloadResult == False:
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
            ProgramDescription = '[COLOR FF888888]Van[/COLOR] ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' [COLOR FF888888]tot[/COLOR] ' + ProgramTimeEndDateTime.strftime('%H:%M') + ' [COLOR FF888888]op[/COLOR] ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

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
