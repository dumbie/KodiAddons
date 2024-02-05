import download
import func
import metadatainfo
import metadatafunc
import path

def check_tv(listItem, defaultGenre='Televisie'):
    try:
        #Get item properties
        StreamAssetId = listItem.getProperty('StreamAssetId')
        ChannelId = listItem.getProperty('ChannelId')
        ExternalId = listItem.getProperty('ExternalId')
        ChannelName = listItem.getProperty('ChannelName')
        ItemLabel = listItem.getLabel()
        ItemArt = listItem.getArt('thumb')
        ItemGenre = listItem.getVideoInfoTag().getGenre()

        #Download details and get json
        download.download_channels_tv()
        channelJson = metadatafunc.search_channelid_jsontelevision(ChannelId)

        #Set item properties
        if func.string_isnullorempty(StreamAssetId):
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(channelJson)
            listItem.setProperty('StreamAssetId', StreamAssetId)

        if func.string_isnullorempty(ChannelName):
            ChannelName = metadatainfo.channelName_from_json_metadata(channelJson)
            listItem.setProperty('ChannelName', ChannelName)

        if func.string_isnullorempty(ItemLabel):
            listItem.setLabel(ChannelName)

        if func.string_isnullorempty(ExternalId):
            ExternalId = metadatainfo.externalId_from_json_metadata(channelJson)
            listItem.setProperty('ExternalId', ExternalId)

        if func.string_isnullorempty(ItemArt):
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})

        if func.string_isnullorempty(ItemGenre):
            listItem.setInfo('video', {'Genre': defaultGenre})
        return True
    except:
        return False

def check_radio(listItem, defaultGenre='Radio'):
    try:
        #Get item properties
        ChannelId = listItem.getProperty('ChannelId')
        ChannelName = listItem.getProperty('ChannelName')
        StreamUrl = listItem.getProperty('StreamUrl')
        ItemLabel = listItem.getLabel()
        ItemArt = listItem.getArt('thumb')
        ItemGenre = listItem.getVideoInfoTag().getGenre()

        #Download details and get json
        download.download_channels_radio()
        channelJson = metadatafunc.search_channelid_jsonradio(ChannelId)

        #Set item properties
        if func.string_isnullorempty(ChannelName):
            ChannelName = channelJson['name']
            listItem.setProperty('ChannelName', ChannelName)

        if func.string_isnullorempty(StreamUrl):
            StreamUrl = channelJson['stream']
            listItem.setProperty('StreamUrl', StreamUrl)

        if func.string_isnullorempty(ItemLabel):
            listItem.setLabel(ChannelName)

        if func.string_isnullorempty(ItemArt):
            listItem.setArt({'thumb': path.icon_radio(ChannelId), 'icon': path.icon_radio(ChannelId)})

        if func.string_isnullorempty(ItemGenre):
            listItem.setInfo('video', {'Genre': defaultGenre})
        return True
    except:
        return False

def check_program(listItem, metaData=None, defaultGenre='Programma'):
    try:
        #Get item properties
        StreamAssetId = listItem.getProperty('StreamAssetId')
        ProgramName = listItem.getProperty('ProgramName')
        ItemLabel = listItem.getLabel()
        ItemGenre = listItem.getVideoInfoTag().getGenre()

        #Set item properties
        if func.string_isnullorempty(StreamAssetId):
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(metaData)
            listItem.setProperty('StreamAssetId', StreamAssetId)

        if func.string_isnullorempty(ProgramName):
            if metaData == None:
                ProgramName = 'Onbekend programma'
            else:
                ProgramName = metadatainfo.episodetitle_from_json_metadata(metaData['resultObj']['containers'][0])
            listItem.setProperty('ProgramName', ProgramName)

        if func.string_isnullorempty(ItemLabel):
            listItem.setLabel(ProgramName)

        if func.string_isnullorempty(ItemGenre):
            listItem.setInfo('video', {'Genre': defaultGenre})
        return True
    except:
        return False

def check_vod(listItem, metaData=None, defaultGenre='Video on demand'):
    try:
        #Get item properties
        StreamAssetId = listItem.getProperty('StreamAssetId')
        ProgramName = listItem.getProperty('ProgramName')
        ItemLabel = listItem.getLabel()
        ItemGenre = listItem.getVideoInfoTag().getGenre()

        #Set item properties
        if func.string_isnullorempty(StreamAssetId):
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(metaData)
            listItem.setProperty('StreamAssetId', StreamAssetId)

        if func.string_isnullorempty(ProgramName):
            if metaData == None:
                ProgramName = 'Onbekend programma'
            else:
                ProgramName = metadatainfo.episodetitle_from_json_metadata(metaData['resultObj']['containers'][0])
            listItem.setProperty('ProgramName', ProgramName)

        if func.string_isnullorempty(ItemLabel):
            listItem.setLabel(ProgramName)

        if func.string_isnullorempty(ItemGenre):
            listItem.setInfo('video', {'Genre': defaultGenre})
        return True
    except:
        return False

def check_recorded(listItem, defaultGenre='Opname'):
    try:
        #Get item properties
        StreamAssetId = listItem.getProperty('StreamAssetId')
        ProgramName = listItem.getProperty('ProgramName')
        ProgramRecordEventId = listItem.getProperty('ProgramRecordEventId')
        ExternalId = listItem.getProperty('ExternalId')
        ItemLabel = listItem.getLabel()
        ItemArt = listItem.getArt('thumb')
        ItemGenre = listItem.getVideoInfoTag().getGenre()

        #Download details and get json
        download.download_recording_event()
        programJson = metadatafunc.search_programid_jsonrecording_event(ProgramRecordEventId)

        #Set item properties
        if func.string_isnullorempty(StreamAssetId):
            StreamAssetId = metadatainfo.stream_assetid_from_json_metadata(programJson)
            listItem.setProperty('StreamAssetId', StreamAssetId)

        if func.string_isnullorempty(ProgramName):
            ProgramName = metadatainfo.programtitle_from_json_metadata(programJson)
            listItem.setProperty('ProgramName', ProgramName)

        if func.string_isnullorempty(ItemLabel):
            listItem.setLabel(ProgramName)

        if func.string_isnullorempty(ExternalId):
            ExternalId = metadatainfo.externalChannelId_from_json_metadata(programJson)
            listItem.setProperty('ExternalId', ExternalId)

        if func.string_isnullorempty(ItemArt):
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})

        if func.string_isnullorempty(ItemGenre):
            listItem.setInfo('video', {'Genre': defaultGenre})
        return True
    except:
        return False
