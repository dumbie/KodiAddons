import dlrecordingevent
import func
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
        remoteMode = listContainer == None
        list_load_append(listContainerSort, remoteMode)

        #Sort list items
        listContainerSort.sort(key=lambda x: x[1].getProperty('ProgramTimeStart'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer, remoteMode=False):
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
            ProgramDurationSeconds = metadatainfo.programdurationint_from_json_metadata(program) * 60
            ProgramDescription = '[COLOR FF888888]Van[/COLOR] ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' [COLOR FF888888]tot[/COLOR] ' + ProgramTimeEndDateTime.strftime('%H:%M') + ' [COLOR FF888888]op[/COLOR] ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, False, False)

            #Set program details
            if remoteMode == True:
                ProgramDetails = '[COLOR FF888888](' + ProgramTimeStartDateTime.strftime('%H:%M') + ') (' + ProgramTimeStartDateTime.strftime('%d %B') + ')[/COLOR] ' + ProgramDetails
            else:
                ProgramName = ProgramName + ' ' + ProgramDetails

            #Set item icons
            iconDefault = path.icon_television(ExternalId)

            #Set item details
            jsonItem = {
                'ProgramRecordEventId': ProgramRecordEventId,
                'ProgramTimeStart': str(ProgramTimeStartDateTime),
                "ProgramDeltaTimeStart": ProgramDeltaTimeStart,
                "ProgramName": ProgramName,
                "ProgramDescription": ProgramDescription,
                'ItemLabel': ProgramName,
                'ItemInfoVideo': {'MediaType': 'movie', 'Genre': ProgramDetails, 'Tagline': ProgramDetails, 'Title': ProgramName, 'Duration': ProgramDurationSeconds},
                'ItemArt': {'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault},
                'ItemAction': 'action_none'
            }
            dirIsfolder = False
            dirUrl = (var.LaunchUrl + '?json=' + func.dictionary_to_jsonstring(jsonItem)) if remoteMode else ''
            listItem = lifunc.jsonitem_to_listitem(jsonItem)
            listContainer.append((dirUrl, listItem, dirIsfolder))
        except:
            continue
