from datetime import datetime, timedelta
import os
import func
import getset
import hybrid
import metadatainfo
import var

def resources(fileName):
    return os.path.join(var.addonpath, fileName)

def addonstorageuser(fileName):
    return os.path.join(var.addonstorageuser, fileName)

def addonstoragecache(fileName):
    return os.path.join(var.addonstoragecache, fileName)

def requirements():
    return 'https://raw.githubusercontent.com/dumbie/kodirepo/master/plugin.video.xs4allwebbieplayer/requirements/'

def icon_television(externalId):
    if func.string_isnullorempty(externalId):
         return icon_addon('unknown')
    else:
        return 'https://images.tv.kpn.com/logo/' + externalId + '/512.png'

def icon_vod(pictureUrl):
    if func.string_isnullorempty(pictureUrl):
         return icon_addon('unknown')
    else:
        return 'https://images.tv.kpn.com/vod/' + pictureUrl + '/220x325.jpg'

def icon_epg(pictureUrl):
    if func.string_isnullorempty(pictureUrl):
        return icon_addon('unknown')
    else:
        return 'https://images.tv.kpn.com/epg/' + pictureUrl + '/220x325.jpg'

def icon_addon(iconName):
    if func.string_isnullorempty(iconName):
        return resources('resources/skins/default/media/common/unknown.png')
    else:
        return resources('resources/skins/default/media/common/' + iconName + '.png')

def icon_fanart():
    return resources('resources/fanart.jpg')

def api_url_web(arguments):
    return 'https://' + var.ApiEndpointUrl() + '/101/1.2.0/A/nld/pctv/kpn/' + arguments

def api_url_stb(arguments):
    return 'https://' + var.ApiEndpointUrl() + '/101/1.2.0/A/nld/stb/kpn/' + arguments

def api_endpoint_deviceid():
    return 'https://ausar.tcloud-itv-prd1.prod.aws.kpn.com/public/v1/ear?type=ott&deviceid=' + getset.setting_get('LoginDeviceId120')[:40]

def api_endpoint_number():
    return 'https://ausar.tcloud-itv-prd1.prod.aws.kpn.com/public/v1/ear?type=ott&tan=' + getset.setting_get('LoginUsername')

def api_endpoint_email():
    return 'https://ausar.tcloud-itv-prd1.prod.aws.kpn.com/public/v1/ear?type=ott'

def api_login():
    return api_url_web('USER/SESSIONS/')

def stream_url_tv(channelId, assetId):
    return api_url_web('CONTENT/VIDEOURL/LIVE/' + channelId + '/' + assetId + '/?deviceId=' + getset.setting_get('LoginDeviceId120') + '&profile=' + metadatainfo.stream_targetprofile())

def stream_url_recording(programId, assetId):
    return api_url_web('CONTENT/VIDEOURL/RECORDING/' + programId + '/' + assetId + '/?deviceId=' + getset.setting_get('LoginDeviceId120') + '&profile=' + metadatainfo.stream_targetprofile())

def stream_url_vod(programId, assetId):
    return api_url_web('CONTENT/VIDEOURL/VOD/' + programId + '/' + assetId + '/?deviceId=' + getset.setting_get('LoginDeviceId120') + '&profile=' + metadatainfo.stream_targetprofile())

def stream_url_program(programId, assetId):
    return api_url_web('CONTENT/VIDEOURL/PROGRAM/' + programId + '/' + assetId + '/?deviceId=' + getset.setting_get('LoginDeviceId120') + '&profile=' + metadatainfo.stream_targetprofile())

def detail_vod(programId):
    return api_url_web('CONTENT/DETAIL/VOD/' + programId)

def detail_program(programId):
    return api_url_web('CONTENT/DETAIL/PROGRAM/' + programId)

def recording_profile():
    return api_url_web('USER/PROFILE/RECORDING')

def recording_event_add_remove():
    return api_url_web('CONTENT/RECORDING/EVENT')

def recording_series_add_remove():
    return api_url_web('CONTENT/RECORDING/SERIES')

def channels_list_web():
    downloadPath = api_url_web('TRAY/LIVECHANNELS?dfilter_channels=subscription&from=0&to=9999')

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def channels_list_stb():
    downloadPath = api_url_stb('TRAY/LIVECHANNELS?dfilter_channels=subscription&from=0&to=9999')

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def recording_event():
    downloadPath = api_url_web('TRAY/USER/RECORDING/EVENT?outputFormat=EXTENDED&from=0&to=9999')

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def recording_series():
    downloadPath = api_url_web('TRAY/USER/RECORDING/SERIES?outputFormat=EXTENDED&from=0&to=9999')

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def vod_movies():
    downloadPath = api_url_web('TRAY/SEARCH/VOD?filter_contentSubtype=VOD&dfilter_packageType=SVOD&from=0&to=9999')
    downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def vod_series():
    downloadPath = api_url_web('TRAY/SEARCH/VOD?filter_contentType=GROUP_OF_BUNDLES&dfilter_packageType=SVOD&from=0&to=9999')
    downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def vod_episodes(parentId):
    downloadPath = api_url_web('TRAY/SEARCH/VOD?filter_parentId=' + parentId + '&from=0&to=9999')

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def vod_kids():
    downloadPath = api_url_web('TRAY/SEARCH/VOD?filter_contentType=GROUP_OF_BUNDLES&dfilter_packageType=SVOD&from=0&to=9999')
    downloadPath += '&filter_genre=kinderen,kids&filter_genres=kinderen,kids'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def program_kids():
    downloadPath = api_url_web('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_includeRegionalChannels=true&from=0&to=9999')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    downloadPath += '&filter_startTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(days=var.VodDayOffsetPast)))
    downloadPath += '&filter_genre=kinderen,kids&filter_genres=kinderen,kids'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def program_sport():
    downloadPath = api_url_web('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_includeRegionalChannels=true&from=0&to=9999')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    downloadPath += '&filter_startTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(days=var.VodDayOffsetPast)))
    downloadPath += '&filter_genre=sport&filter_genres=sport'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def program_movies():
    downloadPath = api_url_web('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_includeRegionalChannels=true&from=0&to=9999')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    downloadPath += '&filter_startTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(days=var.VodDayOffsetPast)))
    downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'
    downloadPath += '&filter_programType=feature+film,short+film,theatre+event,tv+movie'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def program_series():
    downloadPath = api_url_web('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_includeRegionalChannels=true&from=0&to=9999')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    downloadPath += '&filter_startTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(days=var.VodDayOffsetPast)))
    downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'
    includeGenres = 'actie,drama,komisch%20drama,sitcom,mysterie,thriller,horror,misdaad,avontuur,komedie,fantasy,familie,soap,sciencefiction,collectibles,veiling'
    downloadPath += '&filter_genre=' + includeGenres + '&filter_genres=' + includeGenres
    downloadPath += '&filter_programType=miniseries,series'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def program_search(programName):
    programName = hybrid.urllib_quote(programName)
    downloadPath = api_url_web('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&query=' + programName + '&filter_isCatchUp=true&filter_includeRegionalChannels=true&from=0&to=9999')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    downloadPath += '&filter_startTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(days=var.VodDayOffsetPast)))

    if getset.setting_get('SearchFilterFuzzy') == 'true':
        downloadPath += '&filter_fuzzy=true'

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath

def epg_day(dayDateTime):
    #Set download time range
    datetimeMidnight = func.datetime_to_midnight(dayDateTime)
    startTimeEpoch = func.datetime_to_ticks(datetimeMidnight - timedelta(hours=2))
    endTimeEpoch = func.datetime_to_ticks(datetimeMidnight + timedelta(hours=26))
    downloadPath = api_url_web('TRAY/EPG?outputFormat=EXTENDED&filter_startTime=' + str(startTimeEpoch) + '&filter_endTime=' + str(endTimeEpoch) + '&filter_channelIds=' + var.TelevisionChannelIdsPlayableString)

    if getset.setting_get('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_isAdult=false'
    return downloadPath
