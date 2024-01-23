import metadatainfo
from datetime import datetime
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

#Search ProgramIndex for airing program in json epg
def search_programindex_airingtime_jsonepg(jsonEpg, targetTime):
    try:
        if jsonEpg == []: return None
        programIndex = 0
        for Program in jsonEpg['containers']:
            try:
                ProgramTimeEndDateTime = metadatainfo.programenddatetime_from_json_metadata(Program)
                if ProgramTimeEndDateTime < targetTime:
                    programIndex += 1
                else:
                    return programIndex
            except:
                continue
        return None
    except:
        return None

#Search for ChannelId in json recording event
def search_channelid_jsonrecording_event(searchChannelId, filterTime=False):
    try:
        if var.ChannelsDataJsonRecordingEvent == []: return None
        for Record in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
            try:
                if filterTime == True:
                    ProgramTimeEndDateTime = metadatainfo.programenddatetime_generate_from_json_metadata(Record)
                    if datetime.now() > ProgramTimeEndDateTime: continue
                if metadatainfo.channelId_from_json_metadata(Record) == searchChannelId:
                    return Record
            except:
                continue
        return None
    except:
        return None

#Search for ChannelId in json recording series
def search_channelid_jsonrecording_series(searchChannelId):
    try:
        if var.ChannelsDataJsonRecordingSeries == []: return None
        for Record in var.ChannelsDataJsonRecordingSeries["resultObj"]["containers"]:
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
        if var.ChannelsDataJsonRecordingEvent == []: return None
        for Record in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
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
        if var.ChannelsDataJsonRecordingEvent == []: return None
        for Record in var.ChannelsDataJsonRecordingEvent["resultObj"]["containers"]:
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
        if var.ChannelsDataJsonRecordingSeries == []: return None
        for Record in var.ChannelsDataJsonRecordingSeries["resultObj"]["containers"]:
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

#Search for stream asset id by ChannelId
def search_stream_assetid_by_channelid(searchChannelId):
    try:
        channelDetails = search_channelid_jsontelevision(searchChannelId)
        if channelDetails != None:
            return metadatainfo.stream_assetid_from_json_metadata(channelDetails['assets'])
        else:
            return ''
    except:
        return ''

#Search for ChannelId in json television
def search_channelid_jsontelevision(searchChannelId):
    try:
        if var.ChannelsDataJsonTelevision == []: return None
        for Channel in var.ChannelsDataJsonTelevision["resultObj"]["containers"]:
            try:
                if metadatainfo.channelId_from_json_metadata(Channel) == searchChannelId:
                    return Channel
            except:
                continue
        return None
    except:
        return None

#Search for ChannelId in json radio
def search_channelid_jsonradio(searchChannelId):
    try:
        #lengt = str(len(var.ChannelsDataJsonRadio['radios']))
        if var.ChannelsDataJsonRadio == []: return None
        for channel in var.ChannelsDataJsonRadio['radios']:
            try:
                if str(channel['id']) == searchChannelId:
                    return channel
            except:
                continue
        return None
    except:
        return None
