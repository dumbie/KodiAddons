import xbmc
import xbmcgui
import dialog
import download
import func
import metadatainfo
import path
import var

def record_event_epg(_self, listItemSelected, forceRecord=False):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramId = listItemSelected.getProperty('ProgramId')
    ProgramRecordEventId = listItemSelected.getProperty('ProgramRecordEventId')
    ProgramStartDeltaTime = listItemSelected.getProperty('ProgramStartDeltaTime')

    #Check if recording is already set
    if ProgramRecordEventId == '' or forceRecord == True:
        recordAdd = download.record_event_add(ProgramId)
        if recordAdd != '':
            _self.update_channel_record_event_icon(ChannelId)
            _self.update_program_record_event()
            _self.update_channel_record_series_icon(ChannelId)
            _self.update_program_record_series()
    else:
        recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramStartDeltaTime)
        if recordRemove == True:
            _self.update_channel_record_event_icon(ChannelId)
            _self.update_program_record_event()
            _self.update_channel_record_series_icon(ChannelId)
            _self.update_program_record_series()

def record_event_now_television_playergui(listItemSelected):
    ProgramNowId = listItemSelected.getProperty('ProgramNowId')

    #Check the program recording state
    recordProgramEvent = func.search_programid_jsonrecording_event(ProgramNowId)
    if recordProgramEvent:
        ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
        ProgramStartDeltaTime = metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent)
        recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramStartDeltaTime)
        if recordRemove == True:
            listItemSelected.setProperty("ProgramNowRecordEvent", 'false')
    else:
        recordAdd = download.record_event_add(ProgramNowId)
        if recordAdd != '':
            listItemSelected.setProperty("ProgramNowRecordEvent", 'true')

def record_event_next_television_playergui(listItemSelected):
    ProgramNextId = listItemSelected.getProperty('ProgramNextId')

    #Check the program recording state
    recordProgramEvent = func.search_programid_jsonrecording_event(ProgramNextId)
    if recordProgramEvent:
        ProgramRecordEventId = metadatainfo.contentId_from_json_metadata(recordProgramEvent)
        ProgramStartDeltaTime = metadatainfo.programstartdeltatime_from_json_metadata(recordProgramEvent)
        recordRemove = download.record_event_remove(ProgramRecordEventId, ProgramStartDeltaTime)
        if recordRemove == True:
            listItemSelected.setProperty("ProgramNextRecordEvent", 'false')
    else:
        recordAdd = download.record_event_add(ProgramNextId)
        if recordAdd != '':
            listItemSelected.setProperty("ProgramNextRecordEvent", 'true')

def record_series_television_playergui(listItemSelected, forceRecord=False):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramNowRecordSeries = listItemSelected.getProperty('ProgramNowRecordSeries')
    ProgramNowRecordSeriesId = listItemSelected.getProperty('ProgramNowRecordSeriesId')
    ProgramNextRecordSeriesId = listItemSelected.getProperty('ProgramNextRecordSeriesId')

    if ProgramNowRecordSeriesId == '':
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen kan niet worden opgenomen.', notificationIcon, 2500, False)
        return

    if ProgramNowRecordSeries == 'false' or forceRecord == True:
        seriesAdd = download.record_series_add(ChannelId, ProgramNowRecordSeriesId)
        if seriesAdd == True:
            listItemSelected.setProperty('ProgramNowRecordEvent', 'true')
            listItemSelected.setProperty('ProgramNowRecordSeries', 'true')
            if ProgramNextRecordSeriesId == ProgramNowRecordSeriesId:
                listItemSelected.setProperty('ProgramNextRecordEvent', 'true')
                listItemSelected.setProperty('ProgramNextRecordSeries', 'true')
    else:
        #Get the removal series id
        recordProgramSeries = func.search_seriesid_jsonrecording_series(ProgramNowRecordSeriesId)
        if recordProgramSeries:
            ProgramRecordSeriesIdLive = metadatainfo.seriesId_from_json_metadata(recordProgramSeries)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt.', notificationIcon, 2500, False)
            return

        #Ask user to remove recordings
        dialogAnswers = ['Opnames verwijderen', 'Opnames houden']
        dialogHeader = 'Serie opnames verwijderen'
        dialogSummary = 'Wilt u ook alle opnames van deze serie seizoen verwijderen?'
        dialogFooter = ''
        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Opnames verwijderen':
            KeepRecording = False
        elif dialogResult == 'Opnames houden': 
            KeepRecording = True
        else:
            return

        #Remove record series
        seriesRemove = download.record_series_remove(ProgramRecordSeriesIdLive, KeepRecording)
        if seriesRemove == True:
            listItemSelected.setProperty('ProgramNowRecordEvent', 'false')
            listItemSelected.setProperty('ProgramNowRecordSeries', 'false')
            if ProgramNextRecordSeriesId == ProgramNowRecordSeriesId:
                listItemSelected.setProperty('ProgramNextRecordEvent', 'false')
                listItemSelected.setProperty('ProgramNextRecordSeries', 'false')

def record_series_epg(_self, listItemSelected, forceRecord=False):
    ChannelId = listItemSelected.getProperty('ChannelId')
    ProgramRecordSeries = listItemSelected.getProperty('ProgramRecordSeries')
    ProgramRecordSeriesId = listItemSelected.getProperty('ProgramRecordSeriesId')

    if ProgramRecordSeriesId == '':
        notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
        xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen kan niet worden opgenomen.', notificationIcon, 2500, False)
        return

    if ProgramRecordSeries == 'false' or forceRecord == True:
        seriesAdd = download.record_series_add(ChannelId, ProgramRecordSeriesId)
        if seriesAdd == True:
            _self.update_channel_record_event_icon(ChannelId)
            _self.update_program_record_event()
            _self.update_channel_record_series_icon(ChannelId)
            _self.update_program_record_series()
    else:
        #Get the removal series id
        recordProgramSeries = func.search_seriesid_jsonrecording_series(ProgramRecordSeriesId)
        if recordProgramSeries:
            ProgramRecordSeriesIdLive = metadatainfo.seriesId_from_json_metadata(recordProgramSeries)
        else:
            notificationIcon = path.resources('resources/skins/default/media/common/recordseries.png')
            xbmcgui.Dialog().notification(var.addonname, 'Serie seizoen annulering mislukt.', notificationIcon, 2500, False)
            return

        #Ask user to remove recordings
        dialogAnswers = ['Opnames verwijderen', 'Opnames houden']
        dialogHeader = 'Serie opnames verwijderen'
        dialogSummary = 'Wilt u ook alle opnames van deze serie seizoen verwijderen?'
        dialogFooter = ''
        dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
        if dialogResult == 'Opnames verwijderen':
            KeepRecording = False
        elif dialogResult == 'Opnames houden': 
            KeepRecording = True
        else:
            return

        #Remove record series
        seriesRemove = download.record_series_remove(ProgramRecordSeriesIdLive, KeepRecording)
        if seriesRemove == True:
            _self.update_channel_record_event_icon(ChannelId)
            _self.update_program_record_event()
            _self.update_channel_record_series_icon(ChannelId)
            _self.update_program_record_series()
