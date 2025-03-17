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
        jsonString = files.openFileUser("acestream_history.js")
        var.HistoryJson = json.loads(jsonString)
    except:
        var.HistoryJson = []

def clean_history():
    try:
        var.HistoryJson = var.HistoryJson[:100]
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed cleaning history", var.addonicon, 2500, False)

def remove_history(ace_id):
    try:
        #Clean and load json history
        load_history()
        clean_history()

        #Remove ace stream
        removed = False
        for x in var.HistoryJson[:]:
            if x["id"] == ace_id:
                var.HistoryJson.remove(x)
                removed = True

        if removed == True:
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

        #Check ace identifier
        if func.string_isnullorempty(ace_id):
            return

        #Clean and load json history
        load_history()
        clean_history()

        #Insert stream id
        var.HistoryJson.insert(0, {"id": ace_id, "name": ace_id})

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
        clean_history()

        #Set launch handle
        LaunchHandle = int(sys.argv[1])

        #Set icon paths
        iconAdd = func.path_addon('resources/add.png')
        iconPlay = func.path_addon('resources/play.png')
        iconInfo = func.path_addon('resources/info.png')

        #Add default items
        ace_name = "Add ace stream id"
        list_item = xbmcgui.ListItem()
        list_item.setLabel(ace_name)
        list_item.setArt({'thumb': iconAdd, 'icon': iconAdd})
        list_item_url = func.generate_addon_url(action="add")
        xbmcplugin.addDirectoryItem(LaunchHandle, list_item_url, list_item, False)

        ace_name = "Show ace stream info"
        list_item = xbmcgui.ListItem()
        list_item.setLabel(ace_name)
        list_item.setArt({'thumb': iconInfo, 'icon': iconInfo})
        list_item_url = func.generate_addon_url(action="info")
        xbmcplugin.addDirectoryItem(LaunchHandle, list_item_url, list_item, False)

        #Add history items
        for x in var.HistoryJson:
            if x.get("icon"):
                iconPlay = x["icon"]
            ace_id = x["id"]
            ace_name = x["name"]
            list_item = xbmcgui.ListItem()
            list_item.setLabel(ace_name)
            list_item.setArt({'thumb': iconPlay, 'icon': iconPlay})
            list_item.setInfo("video", {'Genre': 'Ace Stream', "Title": ace_name, "Plot": ace_id})
            list_item_url = func.generate_addon_url(action="play", id=ace_id, icon=iconPlay, name=ace_name)

            #Fix add rename stream feature
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

def play_ace_stream(ace_id, ace_icon, ace_name):
    try:
        #Cleanup stream id
        ace_id = ace_id.lower().replace("acestream://", "")

        #Set stream item
        list_item = xbmcgui.ListItem()
        list_item.setLabel(ace_name)
        list_item.setArt({'thumb': ace_icon, 'icon': ace_icon})
        list_item.setInfo("video", {'Genre': 'Ace Stream', "Title": ace_name, "Plot": ace_id})

        #Get stream url
        if getset.setting_get("UseHlsStream") == "false":
            stream_url = "http://127.0.0.1:6878/ace/getstream?id=" + ace_id
            stream_url += "&format=json&force_session_restart=1"
        else:
            stream_url = "http://127.0.0.1:6878/ace/manifest.m3u8?id=" + ace_id
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

        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Playing ace stream " + ace_id, var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed playing ace stream", var.addonicon, 2500, False)

def info_ace_stream():
    try:
        #Get stream settings
        infohash = str(getset.setting_get('infohash'))
        playback_session_id = str(getset.setting_get('playback_session_id'))

        #Download stream info
        info_url = "http://127.0.0.1:6878/ace/stat/" + infohash + "/" + playback_session_id
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
        xbmcgui.Dialog().notification(var.addonname, "Failed info ace stream", var.addonicon, 2500, False)

if __name__ == "__main__":
    argumentDict = dict(hybrid.parse_qsl(sys.argv[2][1:]))
    if argumentDict:
        if argumentDict["action"] == "play":
            play_ace_stream(argumentDict["id"], argumentDict["icon"], argumentDict["name"])
        elif argumentDict["action"] == "add":
            add_history()
        elif argumentDict["action"] == "info":
            info_ace_stream()
        elif argumentDict["action"] == "remove":
            remove_history(argumentDict["id"])
    else:
        list_main()