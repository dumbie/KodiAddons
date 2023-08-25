from datetime import datetime, timedelta
import func
import metadatainfo
import xbmcgui
import path
import var

def list_load(listContainer):
    RecordingEvents = var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]
    RecordingEvents = sorted(RecordingEvents, key=lambda x: x['metadata']['programStartTime'], reverse=False)

    #Process all the planned recording
    for program in RecordingEvents:
        try:
            #Load program basics
            ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(program)

            #Check if recording is planned or already recorded
            if ProgramTimeEndDateTime < datetime.now(): continue

            #Load program details
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(program)
            ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(program)
            ProgramStartDeltaTime = str(metadatainfo.programstartdeltatime_from_json_metadata(program))
            ProgramName = metadatainfo.programtitle_from_json_metadata(program)
            ProgramTimeStartDateTime = metadatainfo.programstartdatetime_from_json_metadata(program)
            ProgramYear = metadatainfo.programyear_from_json_metadata(program)
            ProgramSeason = metadatainfo.programseason_from_json_metadata(program)
            ProgramEpisode = metadatainfo.episodenumber_from_json_metadata(program)
            ProgramDescription = 'Van ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' tot ' + ProgramTimeEndDateTime.strftime('%H:%M') + ' op ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            #Combine program details
            stringJoin = [ ProgramYear, ProgramSeason, ProgramEpisode ]
            ProgramDetails = ' '.join(filter(None, stringJoin))
            if func.string_isnullorempty(ProgramDetails):
                ProgramDetails = '(?)'

            #Update program name string
            ProgramName += ' [COLOR gray]' + ProgramDetails + '[/COLOR]'

            #Add recording event to the list
            listitem = xbmcgui.ListItem()
            listitem.setProperty('ProgramRecordEventId', ProgramRecordEventId)
            listitem.setProperty('ProgramStartDeltaTime', ProgramStartDeltaTime)
            listitem.setProperty('ProgramName', ProgramName)
            listitem.setProperty('ProgramDescription', ProgramDescription)
            listitem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.addItem(listitem)
        except:
            continue
