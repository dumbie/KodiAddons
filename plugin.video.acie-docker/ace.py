import json
import getset
import history
import func
import var
import hybrid
import xbmc
import xbmcgui

def play_ace_stream(ace_id, ace_icon, ace_title):
    try:
        #Check stream title
        if ace_title == "Unknown" or func.string_isnullorempty(ace_title):
            ace_title = get_title_ace_stream(ace_id)
            history.update_history_title(ace_id, ace_title)

        #Check stream icon
        if func.string_isnullorempty(ace_icon):
            ace_icon = func.path_addon('resources/play.png')

        #Set stream item
        list_item = xbmcgui.ListItem()
        list_item.setLabel(ace_title)
        list_item.setArt({'thumb': ace_icon, 'icon': ace_icon})
        list_item.setInfo("video", {'Genre': 'Ace Stream', "Title": ace_title, "Plot": ace_id})

        #Get stream settings
        ace_ip = str(getset.setting_get('AceIp'))
        ace_port = str(getset.setting_get('AcePort'))

        #Get stream url
        if getset.setting_get("UseHlsStream") == "false":
            stream_url = "http://" + ace_ip + ":" + ace_port + "/ace/getstream?id=" + ace_id
            stream_url += "&format=json&force_session_restart=1"
        else:
            stream_url = "http://" + ace_ip + ":" + ace_port + "/ace/manifest.m3u8?id=" + ace_id
            stream_url += "&format=json&force_session_restart=1&transcode_audio=1&preferred_audio_language=ENG"

        #Download stream info
        downloadRequest = hybrid.urllib_request(stream_url)
        downloadDataHttp = hybrid.urllib_urlopen(downloadRequest)
        downloadJson = json.load(downloadDataHttp)
        if downloadJson['response']:
            infohash = str(downloadJson['response']['infohash'])
            playback_session_id = str(downloadJson['response']['playback_session_id'])
            stream_url = str(downloadJson['response']['playback_url'])
        else:
            #Notification
            xbmcgui.Dialog().notification(var.addonname, "Ace stream id not available", var.addonicon, 2500, False)
            return

        #Set stream settings
        getset.setting_set('infohash', infohash)
        getset.setting_set('playback_session_id', playback_session_id)

        #Set input stream
        if getset.setting_get("UseHlsStream") == "false":
            if getset.setting_get("UseInputStream") == "true":
                list_item.setProperty(hybrid.inputstreamname, 'inputstream.ffmpegdirect')
                list_item.setProperty('inputstream.ffmpegdirect.manifest_type', 'ts')
                list_item.setMimeType('video/mp2t')
                list_item.setContentLookup(False)
        else:
            if getset.setting_get("UseInputStream") == "true":
                #list_item.setProperty(hybrid.inputstreamname, 'inputstream.ffmpegdirect')
                #list_item.setProperty('inputstream.ffmpegdirect.manifest_type', 'hls')
                list_item.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
                list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
                list_item.setMimeType('application/vnd.apple.mpegurl')
                list_item.setContentLookup(False)

        #Play stream url
        xbmc.Player().play(stream_url, list_item, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed playing ace stream", var.addonicon, 2500, False)

def get_title_ace_stream(ace_id):
    try:
        #Get stream settings
        ace_ip = str(getset.setting_get('AceIp'))
        ace_port = str(getset.setting_get('AcePort'))

        #Download stream title
        info_url = "http://" + ace_ip + ":" + ace_port  + "/server/api?method=analyze_content&query=acestream%3A%3Fcontent_id%3D" + ace_id
        downloadRequest = hybrid.urllib_request(info_url)
        downloadDataHttp = hybrid.urllib_urlopen(downloadRequest)
        downloadJson = json.load(downloadDataHttp)

        #Set stream title
        stream_title = str(downloadJson['result']['title'])

        #Check and return stream title
        if func.string_isnullorempty(stream_title):
            return "Unknown"
        else:
            return stream_title
    except:
        return "Unknown"

def show_info_ace_stream():
    try:
        #Get stream settings
        infohash = str(getset.setting_get('infohash'))
        playback_session_id = str(getset.setting_get('playback_session_id'))
        ace_ip = str(getset.setting_get('AceIp'))
        ace_port = str(getset.setting_get('AcePort'))

        #Download stream info
        info_url = "http://" + ace_ip + ":" + ace_port + "/ace/stat/" + infohash + "/" + playback_session_id
        downloadRequest = hybrid.urllib_request(info_url)
        downloadDataHttp = hybrid.urllib_urlopen(downloadRequest)
        downloadJson = json.load(downloadDataHttp)

        #Set stream info
        if downloadJson['response']:
            speed_download = str(downloadJson['response']['speed_down'])
            speed_upload = str(downloadJson['response']['speed_up'])
            peers = str(downloadJson['response']['peers'])
            info_string = "(DL) " + speed_download + " (UL) " + speed_upload + " (P) " + peers

            #Notification
            xbmcgui.Dialog().notification(var.addonname, info_string, var.addonicon, 2500, False)
        else:
            #Notification
            xbmcgui.Dialog().notification(var.addonname, "No stream running", var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed getting ace stream info", var.addonicon, 2500, False)
