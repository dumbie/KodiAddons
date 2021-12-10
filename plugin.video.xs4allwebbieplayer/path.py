import os
import time
from datetime import datetime, timedelta
import func
import var

def resources(fileName):
    return os.path.join(var.addonpath, fileName)

def addonstorage(fileName):
    return os.path.join(var.addonstorage, fileName)

def requirements():
    return 'https://raw.githubusercontent.com/dumbie/kodirepo/master/plugin.video.xs4allwebbieplayer/requirements/'

def icon_television(externalId):
    return 'https://images.tv.kpn.com/logo/' + externalId + '/512.png'

def icon_vod(pictureUrl):
    return 'https://images.tv.kpn.com/vod/' + pictureUrl + '/220x325.jpg'

def icon_epg(pictureUrl):
    return 'https://images.tv.kpn.com/epg/' + pictureUrl + '/220x325.jpg'

def icon_radio(channelId):
    return 'https://raw.githubusercontent.com/dumbie/kodirepo/master/plugin.video.xs4allwebbieplayer/radio/' + channelId + '.png'

def api_url_120(arguments):
    return 'https://api.tv.kpn.com/101/1.2.0/A/nld/pctv/kpn/' + arguments

def api_login():
    return api_url_120('USER/SESSIONS/')

def stream_url_tv(channelId, assetId):
    return api_url_120('CONTENT/VIDEOURL/LIVE/' + channelId + '/' + assetId + '/?deviceId=' + var.addon.getSetting('LoginDeviceId120') + '&profile=G04')

def stream_url_recording(programId, assetId):
    return api_url_120('CONTENT/VIDEOURL/RECORDING/' + programId + '/' + assetId + '/?deviceId=' + var.addon.getSetting('LoginDeviceId120') + '&profile=G04')

def stream_url_vod(programId, assetId):
    return api_url_120('CONTENT/VIDEOURL/VOD/' + programId + '/' + assetId + '/?deviceId=' + var.addon.getSetting('LoginDeviceId120') + '&profile=G04')

def stream_url_program(programId, assetId):
    return api_url_120('CONTENT/VIDEOURL/PROGRAM/' + programId + '/' + assetId + '/?deviceId=' + var.addon.getSetting('LoginDeviceId120') + '&profile=G04')

def userdata_vod(programId):
    return api_url_120('CONTENT/USERDATA/VOD/' + programId)

def userdata_program(programId):
    return api_url_120('CONTENT/USERDATA/PROGRAM/' + programId)

def channels_list_radio():
    return 'https://raw.githubusercontent.com/dumbie/kodirepo/master/plugin.video.xs4allwebbieplayer/radio/listradios.js'

def channels_list_tv():
    return api_url_120('TRAY/LIVECHANNELS/?orderBy=orderId&sortOrder=asc&dfilter_channels=subscription&from=0&to=9999')

def recording_event_add_remove():
    return api_url_120('CONTENT/RECORDING/EVENT')

def recording_series_add_remove():
    return api_url_120('CONTENT/RECORDING/SERIES')

def recording_event():
    return api_url_120('TRAY/USER/RECORDING/EVENT?outputFormat=EXTENDED&sortOrder=desc&orderBy=StartTime&from=0&to=9999')

def recording_series():
    return api_url_120('TRAY/USER/RECORDING/SERIES?sortOrder=desc&orderBy=StartTime&from=0&to=9999')

def vod_yesterday():
    #Set download time range
    dateTimeMidnight = func.datetime_to_midnight(datetime.now())
    startTimeEpoch = func.datetime_to_ticks(dateTimeMidnight - timedelta(days=1), True)
    endTimeEpoch = func.datetime_to_ticks(dateTimeMidnight + timedelta(hours=1), True)

    downloadPath = api_url_120('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_fuzzy=true&from=0&to=9999')
    downloadPath += '&filter_airingStartTime=' + str(startTimeEpoch) + '&filter_airingEndTime=' + str(endTimeEpoch)
    if var.addon.getSetting('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_excludedGenre=kinderen,kids,erotiek&filter_excludedGenres=kinderen,kids,erotiek'
    else:
        downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'
    return downloadPath

def vod_movies():
    downloadPath = api_url_120('TRAY/SEARCH/VOD?filter_contentSubtype=VOD&dfilter_packageType=SVOD&from=0&to=9999')
    if var.addon.getSetting('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_excludedGenre=kinderen,kids,erotiek&filter_excludedGenres=kinderen,kids,erotiek'
    else:
        downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'
    return downloadPath

def vod_series():
    downloadPath = api_url_120('TRAY/SEARCH/VOD?filter_contentType=GROUP_OF_BUNDLES&dfilter_packageType=SVOD&from=0&to=9999')
    if var.addon.getSetting('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_excludedGenre=kinderen,kids,erotiek&filter_excludedGenres=kinderen,kids,erotiek'
    else:
        downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'
    return downloadPath

def vod_series_kids():
    downloadPath = api_url_120('TRAY/SEARCH/VOD?filter_contentType=GROUP_OF_BUNDLES&dfilter_packageType=SVOD&from=0&to=9999&filter_genres=kinderen,kids')
    return downloadPath

def vod_series_season(parentId):
    return api_url_120('TRAY/SEARCH/VOD?filter_parentId=' + parentId + '&from=0&to=9999')

def search_sport():
    downloadPath = api_url_120('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_fuzzy=true&from=0&to=9999&filter_genre=sport')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    return downloadPath

def search_kids():
    downloadPath = api_url_120('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_fuzzy=true&from=0&to=9999&filter_genre=kinderen,kids')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    return downloadPath

def search_movies():
    downloadPath = api_url_120('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_fuzzy=true&from=0&to=9999&filter_programType=film')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    if var.addon.getSetting('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_excludedGenre=kinderen,kids,erotiek&filter_excludedGenres=kinderen,kids,erotiek'
    else:
        downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'
    return downloadPath

def search_series():
    downloadPath = api_url_120('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&filter_isTvPremiere=true&filter_isCatchUp=true&filter_fuzzy=true&from=0&to=9999&filter_programType=serie')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    if var.addon.getSetting('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_excludedGenre=kinderen,kids,erotiek&filter_excludedGenres=kinderen,kids,erotiek'
    else:
        downloadPath += '&filter_excludedGenre=kinderen,kids&filter_excludedGenres=kinderen,kids'
    return downloadPath

def search_program(programName):
    downloadPath = api_url_120('TRAY/SEARCH/PROGRAM?outputFormat=EXTENDED&dfilter_channels=subscription&query=' + programName + '&filter_isTvPremiere=true&filter_isCatchUp=true&filter_fuzzy=true&from=0&to=9999&orderBy=airingStartTime&sortOrder=desc')
    downloadPath += '&filter_endTime=' + str(func.datetime_to_ticks(datetime.utcnow() - timedelta(minutes=var.RecordingProcessMinutes)))
    if var.addon.getSetting('TelevisionChannelNoErotic') == 'true':
        downloadPath += '&filter_excludedGenre=erotiek'
    return downloadPath

def epg_day(dateStringDay):
    #Get all playable channel ids
    ChannelIdsPlayableString = ''
    for playableId in var.ChannelIdsPlayable:
        ChannelIdsPlayableString += playableId + ','
    ChannelIdsPlayableString = ChannelIdsPlayableString[:-1]

    #Set download time range
    datetimeMidnight = func.datetime_from_string(dateStringDay, '%Y-%m-%d')
    startTimeEpoch = func.datetime_to_ticks(datetimeMidnight - timedelta(hours=6))
    endTimeEpoch = func.datetime_to_ticks(datetimeMidnight + timedelta(hours=30))

    return api_url_120('TRAY/EPG?outputFormat=EXTENDED&filter_startTime=' + str(startTimeEpoch) + '&filter_endTime=' + str(endTimeEpoch) + '&filter_channelIds=' + ChannelIdsPlayableString)
