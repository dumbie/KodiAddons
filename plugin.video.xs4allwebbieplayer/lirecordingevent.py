from datetime import datetime, timedelta
import download
import lifunc
import metadatacombine
import metadatainfo
import xbmcgui
import path
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
        listContainerSort.sort(key=lambda x: int(x.getProperty('ProgramStartTime')))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    #Set the current player play time
    dateTimeNow = datetime.now()

    for program in var.RecordingEventDataJson["resultObj"]["containers"]:
        try:
            #Load program basics
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)

            #Check if recording is planned or already recorded
            if ProgramTimeEndDateTime < dateTimeNow: continue

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramStartTime = str(metadatainfo.programstarttime_from_json_metadata(program))
            ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(program))
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramDescription = 'Van ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' tot ' + ProgramTimeEndDateTime.strftime('%H:%M') + ' op ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            #Combine program details
            ProgramDetails = metadatacombine.program_details(program, True, False, True, True, True, False, False)

            #Update program name string
            ProgramName += ' ' + ProgramDetails

            #Add recording event to the list
            listItem = xbmcgui.ListItem()
            listItem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
            listItem.setProperty('ProgramStartTime', ProgramStartTime)
            listItem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.append(listItem)
        except:
            continue
