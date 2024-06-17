import metadatainfo
import recordingfunc
import var

#Search for ChannelId in json epg
def search_channelid_jsonepg(jsonEpg, searchChannelId):
    try:
        if jsonEpg == []: return None
        for Epg in jsonEpg["resultObj"]["containers"]:
            try:
                if metadatainfo.channelId_from_json_metadata(Epg) == searchChannelId:
                    return Epg
            except:
                continue
        return None
    except:
        return None

#Search Program for airing program in json epg
def search_program_airingtime_jsonepg(jsonEpg, targetTime):
    try:
        if jsonEpg == []: return None
        for Program in jsonEpg['containers']:
            try:
                if metadatainfo.programenddatetime_from_json_metadata(Program) > targetTime:
                    return Program
            except:
                continue
        return None
    except:
        return None

#Search ProgramIndex for airing program in json epg
def search_programindex_airingtime_jsonepg(jsonEpg, targetTime):
    try:
        if jsonEpg == []: return None
        programIndex = 0
        for Program in jsonEpg['containers']:
            try:
                if metadatainfo.programenddatetime_from_json_metadata(Program) < targetTime:
                    programIndex += 1
                else:
                    return programIndex
            except:
                continue
        return None
    except:
        return None

#Search for ChannelId in json recording event
def search_channelid_jsonrecording_event(searchChannelId, scheduledOnly=False):
    try:
        if var.RecordingEventDataJson == []: return None
        for Record in var.RecordingEventDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.channelId_from_json_metadata(Record) != searchChannelId: continue
                if scheduledOnly == True and recordingfunc.check_status_scheduled(Record) == False:
                    return None
                else:
                    return Record
            except:
                continue
        return None
    except:
        return None

#Search for ChannelId in json recording series
def search_channelid_jsonrecording_series(searchChannelId):
    try:
        if var.RecordingSeriesDataJson == []: return None
        for Record in var.RecordingSeriesDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.channelId_from_json_metadata(Record) == searchChannelId:
                    return Record
            except:
                continue
        return None
    except:
        return None

#Search for ProgramId in json recording event
def search_programid_jsonrecording_event(searchProgramId):
    try:
        if var.RecordingEventDataJson == []: return None
        for Record in var.RecordingEventDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.contentId_from_json_metadata(Record) == searchProgramId:
                    return Record
                if metadatainfo.contentIdLive_from_json_metadata(Record) == searchProgramId:
                    return Record
            except:
                continue
        return None
    except:
        return None

#Search for SeriesId in json recording event
def search_seriesid_jsonrecording_event(searchSeriesId):
    try:
        if var.RecordingEventDataJson == []: return None
        for Record in var.RecordingEventDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.seriesId_from_json_metadata(Record) == searchSeriesId:
                    return Record
                if metadatainfo.seriesIdLive_from_json_metadata(Record) == searchSeriesId:
                    return Record
            except:
                continue
        return None
    except:
        return None

#Search for SeriesId in json recording series
def search_seriesid_jsonrecording_series(searchSeriesId):
    try:
        if var.RecordingSeriesDataJson == []: return None
        for Record in var.RecordingSeriesDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.seriesId_from_json_metadata(Record) == searchSeriesId:
                    return Record
                if metadatainfo.seriesIdLive_from_json_metadata(Record) == searchSeriesId:
                    return Record
            except:
                continue
        return None
    except:
        return None

#Search for ChannelId in json web
def search_channelid_json_web(searchChannelId):
    try:
        if var.WebChannelsDataJson == []: return None
        for channel in var.WebChannelsDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.channelId_from_json_metadata(channel) == searchChannelId:
                    return channel
            except:
                continue
        return None
    except:
        return None

#Search for ChannelId in json stb
def search_channelid_json_stb(searchChannelId):
    try:
        if var.StbChannelsDataJson == []: return None
        for channel in var.StbChannelsDataJson["resultObj"]["containers"]:
            try:
                if metadatainfo.channelId_from_json_metadata(channel) == searchChannelId:
                    return channel
            except:
                continue
        return None
    except:
        return None
