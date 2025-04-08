import sys
import json
import getset
import files
import func
import var
import hybrid
import xbmc
import xbmcgui
import xbmcplugin

def load_history():
    try:
        #Load file to string
        jsonString = files.openFileUser("acestream_history.js")

        #Convert string to json
        var.HistoryJson = json.loads(jsonString)

        #Limit loaded items
        history_limit = int(getset.setting_get("HistoryLimit"))
        if history_limit > 0:
            var.HistoryJson = var.HistoryJson[:history_limit]
    except:
        var.HistoryJson = []

def update_history_title(ace_id, ace_title):
    try:
        #Clean and load json history
        load_history()

        #Update ace stream
        updatedJson = False
        for x in var.HistoryJson[:]:
            if x["id"] == ace_id:
                x["title"] = ace_title
                updatedJson = True

        if updatedJson == True:
            #Save history
            JsonDumpBytes = json.dumps(var.HistoryJson).encode("ascii")
            files.saveFileUser("acestream_history.js", JsonDumpBytes)

            #Refresh list
            xbmc.executebuiltin("Container.Refresh")
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed updating ace stream title", var.addonicon, 2500, False)

def remove_history(ace_id, saveJson=True):
    try:
        #Clean and load json history
        load_history()

        #Remove ace stream
        updatedJson = False
        for x in var.HistoryJson[:]:
            if x["id"] == ace_id:
                var.HistoryJson.remove(x)
                updatedJson = True

        if updatedJson == True and saveJson == True:
            #Save history
            JsonDumpBytes = json.dumps(var.HistoryJson).encode("ascii")
            files.saveFileUser("acestream_history.js", JsonDumpBytes)

            #Refresh list
            xbmc.executebuiltin("Container.Refresh")

            #Notification
            xbmcgui.Dialog().notification(var.addonname, "Removed ace stream id", var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed removing ace stream id", var.addonicon, 2500, False)

def add_history():
    try:
        #Show keyboard
        keyboard = xbmc.Keyboard("default", "heading")
        keyboard.setHeading("Add ace stream id")
        keyboard.setDefault("")
        keyboard.setHiddenInput(False)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            ace_id = keyboard.getText()
        else:
            return

        #Check stream id empty
        if func.string_isnullorempty(ace_id):
            xbmcgui.Dialog().notification(var.addonname, "Empty ace stream id", var.addonicon, 2500, False)
            return

        #Check stream id length
        if len(ace_id) < 40:
            xbmcgui.Dialog().notification(var.addonname, "Invalid ace stream id", var.addonicon, 2500, False)
            return

        #Cleanup stream id
        ace_id = ace_id.strip()
        ace_id = ace_id.lower()
        ace_id = ace_id.replace("acestream://", "")
        if "?id=" in ace_id:
            ace_id = ace_id.split("?id=")[1]

        #Check stream id length
        if len(ace_id) > 40:
            xbmcgui.Dialog().notification(var.addonname, "Invalid ace stream id", var.addonicon, 2500, False)
            return

        #Clean and load json history
        load_history()

        #Remove double stream id
        remove_history(ace_id, saveJson=False)

        #Insert stream id
        var.HistoryJson.insert(0, {"id": ace_id, "icon": "", "title": ""})

        #Save history
        JsonDumpBytes = json.dumps(var.HistoryJson).encode("ascii")
        files.saveFileUser("acestream_history.js", JsonDumpBytes)

        #Refresh list
        xbmc.executebuiltin("Container.Refresh")

        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Added ace stream id", var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed adding ace stream id", var.addonicon, 2500, False)

def list_main():
    try:
        #Clean and load json history
        load_history()

        #Set launch handle
        LaunchHandle = int(sys.argv[1])

        #Set icon paths
        iconAdd = func.path_addon('resources/add.png')
        iconInfo = func.path_addon('resources/info.png')

        #Add default items
        list_label = "Add ace stream id"
        list_item = xbmcgui.ListItem()
        list_item.setLabel(list_label)
        list_item.setArt({'thumb': iconAdd, 'icon': iconAdd})
        list_item_url = func.generate_addon_url(action="add")
        xbmcplugin.addDirectoryItem(LaunchHandle, list_item_url, list_item, False)

        list_label = "Show ace stream info"
        list_item = xbmcgui.ListItem()
        list_item.setLabel(list_label)
        list_item.setArt({'thumb': iconInfo, 'icon': iconInfo})
        list_item_url = func.generate_addon_url(action="info")
        xbmcplugin.addDirectoryItem(LaunchHandle, list_item_url, list_item, False)

        #Add history items
        for x in var.HistoryJson:
            ace_id = x["id"]
            if x.get("icon"):
                ace_icon = x["icon"]
            else:
                ace_icon = func.path_addon('resources/play.png')
            if x.get("title"):
                ace_title = x["title"]
            else:
                ace_title = " "
                #Fix load stream title here?

            list_item = xbmcgui.ListItem()
            list_item.setLabel(ace_id + " [COLOR grey]" + ace_title + "[/COLOR]")
            list_item.setArt({'thumb': ace_icon, 'icon': ace_icon})
            list_item.setInfo("video", {'Genre': 'Ace Stream', "Title": ace_title, "Plot": ace_id})
            list_item_url = func.generate_addon_url(action="play", id=ace_id, icon=ace_icon, title=ace_title)

            context_items = []
            context_name = "Remove ace stream id"
            context_run = 'RunPlugin(' + func.generate_addon_url(action="remove", id=ace_id) + ')'
            context_items.append((context_name, context_run))
            list_item.addContextMenuItems(context_items)

            xbmcplugin.addDirectoryItem(LaunchHandle, list_item_url, list_item, False)

        #Finalize item directory
        xbmcplugin.endOfDirectory(LaunchHandle)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed listing items", var.addonicon, 2500, False)

def play_ace_stream(ace_id, ace_icon, ace_title):
    try:
        #Check stream title
        if func.string_isnullorempty(ace_title):
            ace_title = get_title_ace_stream(ace_id)
            update_history_title(ace_id, ace_title)

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
            return ace_id
        else:
            return stream_title
    except:
        return ace_id

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

if __name__ == "__main__":
    argumentDict = dict(hybrid.parse_qsl(sys.argv[2][1:]))
    if argumentDict:
        if argumentDict["action"] == "play":
            play_ace_stream(argumentDict["id"], argumentDict["icon"], argumentDict["title"])
        elif argumentDict["action"] == "add":
            add_history()
        elif argumentDict["action"] == "info":
            show_info_ace_stream()
        elif argumentDict["action"] == "remove":
            remove_history(argumentDict["id"])
    else:
        list_main()