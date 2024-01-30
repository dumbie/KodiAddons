import re
import metadatainfo
import hybrid
import var
import xbmc

#Update stream url with bitrate setting
def adjust_streamurl_bitrate(streamUrl):
    if "&min_bitrate=" in streamUrl:
        streamUrl = re.sub("&min_bitrate=([0-9]+)", "&min_bitrate=0", streamUrl)
    else:
        streamUrl += "&min_bitrate=0"
    if "&max_bitrate=" in streamUrl:
        streamUrl = re.sub("&max_bitrate=([0-9]+)", "&max_bitrate=" + metadatainfo.stream_targetbitrate(), streamUrl)
    else:
        streamUrl += "&max_bitrate=" + metadatainfo.stream_targetbitrate()
    return streamUrl

#Update stream url with localhost proxy
def adjust_streamurl_proxy(streamUrl):
    if xbmc.getCondVisibility('System.Platform.Android') or var.addon.getSetting('UseLocalhostProxy') == 'true':
        return 'http://127.0.0.1:4444/redir/' + str(streamUrl)
    else:
        return streamUrl

#Update listitem with input stream properties
def adjust_listitem_properties(listItem):
    try:
        #Set internet stream property
        listItem.setProperty("get_stream_details_from_player", 'true')
    except:
        pass

#Update listitem with input stream properties
def adjust_listitem_inputstream(listItem, downloadDataJson, liveStream=False):
    try:
        #Set stream headers dictionary
        StreamHeadersDict = {
            "User-Agent": var.addon.getSetting('CustomUserAgent')
        }

        #Set stream headers string
        StreamHeadersString = ''
        for name, value in StreamHeadersDict.items():
            StreamHeadersString += '&' + name + '=' + hybrid.urllib_quote(value)
        StreamHeadersString = StreamHeadersString.replace('&', '', 1)

        #Set input adaptive properties
        listItem.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
        listItem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
        listItem.setProperty('inputstream.adaptive.stream_headers', StreamHeadersString)
        listItem.setMimeType('application/xml+dash')
        listItem.setContentLookup(False)

        #Set input adaptive live property
        if liveStream:
            listItem.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')

        #Get and set stream license key
        AdaptiveLicenseUrl = downloadDataJson['resultObj']['src']['sources']['contentProtection']['widevine']['licenseAcquisitionURL']
        AdaptivePostData = 'R{SSM}'
        AdaptiveResponse = ''
        listItem.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
        listItem.setProperty('inputstream.adaptive.license_key', AdaptiveLicenseUrl + "|" + StreamHeadersString + "|" + AdaptivePostData + "|" + AdaptiveResponse)
    except:
        pass
