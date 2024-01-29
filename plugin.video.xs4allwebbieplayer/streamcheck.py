import download
import func
import metadatainfo
import metadatafunc
import path

def check_tv(listItem, defaultGenre='Televisie'):
    try:
        #Get item properties
        AssetId = listItem.getProperty('AssetId')
        ChannelId = listItem.getProperty('ChannelId')
        ExternalId = listItem.getProperty('ExternalId')
        ChannelName = listItem.getProperty('ChannelName')
        ItemLabel = listItem.getLabel()
        ItemArt = listItem.getArt('thumb')
        ItemVideoInfo = listItem.getVideoInfoTag()
        ItemGenres = ItemVideoInfo.getGenres()

        #Download details and get json
        download.download_channels_tv()
        channelJson = metadatafunc.search_channelid_jsontelevision(ChannelId)

        #Set item properties
        if func.string_isnullorempty(AssetId):
            AssetId = metadatainfo.stream_assetid_from_json_metadata(channelJson)
            listItem.setProperty('AssetId', AssetId)

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

        if ItemGenres == []:
            ItemVideoInfo.setGenres([defaultGenre])
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
        ItemVideoInfo = listItem.getVideoInfoTag()
        ItemGenres = ItemVideoInfo.getGenres()

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

        if ItemGenres == []:
            ItemVideoInfo.setGenres([defaultGenre])
        return True
    except:
        return False

def check_program(listItem, defaultGenre='Programma'):
    try:
        #Get item properties
        ProgramId = listItem.getProperty('ProgramId')
        ProgramName = listItem.getProperty('ProgramName')
        ItemLabel = listItem.getLabel()
        ItemVideoInfo = listItem.getVideoInfoTag()
        ItemGenres = ItemVideoInfo.getGenres()

        #Set item properties
        if func.string_isnullorempty(ProgramName):
            ProgramName = 'Onbekend programma'
            listItem.setProperty('ProgramName', ProgramName)

        if func.string_isnullorempty(ItemLabel):
            listItem.setLabel(ProgramName)

        if ItemGenres == []:
            ItemVideoInfo.setGenres([defaultGenre])
        return True
    except:
        return False

def check_vod(listItem, defaultGenre='Video on demand'):
    try:
        #Get item properties
        ProgramId = listItem.getProperty('ProgramId')
        ProgramName = listItem.getProperty('ProgramName')
        ItemLabel = listItem.getLabel()
        ItemVideoInfo = listItem.getVideoInfoTag()
        ItemGenres = ItemVideoInfo.getGenres()

        #Set item properties
        if func.string_isnullorempty(ProgramName):
            ProgramName = 'Onbekend programma'
            listItem.setProperty('ProgramName', ProgramName)

        if func.string_isnullorempty(ItemLabel):
            listItem.setLabel(ProgramName)

        if ItemGenres == []:
            ItemVideoInfo.setGenres([defaultGenre])
        return True
    except:
        return False

def check_recorded(listItem, defaultGenre='Opname'):
    try:
        #Get item properties
        ProgramName = listItem.getProperty('ProgramName')
        ProgramRecordEventId = listItem.getProperty('ProgramRecordEventId')
        ExternalId = listItem.getProperty('ExternalId')
        ItemLabel = listItem.getLabel()
        ItemArt = listItem.getArt('thumb')
        ItemVideoInfo = listItem.getVideoInfoTag()
        ItemGenres = ItemVideoInfo.getGenres()

        #Download details and get json
        download.download_recording_event()
        programJson = metadatafunc.search_programid_jsonrecording_event(ProgramRecordEventId)

        #Set item properties
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

        if ItemGenres == []:
            ItemVideoInfo.setGenres([defaultGenre])
        return True
    except:
        return False
