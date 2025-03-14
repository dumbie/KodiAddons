import os
import sys
import getpass
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

        #Set icon paths
        iconAdd = func.path_addon('resources/add.png')
        iconPlay = func.path_addon('resources/play.png')

        #Add default item
        ace_name = "Add ace stream id"
        list_item = xbmcgui.ListItem()
        list_item.setLabel(ace_name)
        list_item.setArt({'thumb': iconAdd, 'icon': iconAdd})
        list_item_url = func.generate_addon_url(action="add")
        xbmcplugin.addDirectoryItem(var.LaunchHandle, list_item_url, list_item, False)

        #Add history items
        for x in var.HistoryJson:
            ace_id = x["id"]
            ace_name = x["name"]
            list_item = xbmcgui.ListItem()
            list_item.setLabel(ace_name)
            list_item.setArt({'thumb': iconPlay, 'icon': iconPlay})
            list_item.setInfo("video", {'Genre': 'Ace Stream', "Title": ace_name})
            list_item_url = func.generate_addon_url(action="play", name=ace_name, id=ace_id)
            xbmcplugin.addDirectoryItem(var.LaunchHandle, list_item_url, list_item, False)

        #Finalize item directory
        xbmcplugin.endOfDirectory(var.LaunchHandle)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed listing items", var.addonicon, 2500, False)

def play_ace_stream(ace_name, ace_id):
    try:
        #Cleanup stream id
        ace_id = ace_id.lower().replace("acestream://", "")

        #Set icon paths
        iconPlay = func.path_addon('resources/play.png')

        #Set stream item
        list_item = xbmcgui.ListItem()
        list_item.setLabel(ace_name)
        list_item.setArt({'thumb': iconPlay, 'icon': iconPlay})
        list_item.setInfo("video", {'Genre': 'Ace Stream', "Title": ace_name})

        #Set stream url
        if getset.setting_get("UseHlsStream") == "false":
            stream_url = "http://127.0.0.1:6878/ace/getstream?id=" + ace_id
            if getset.setting_get("UseInputStream") == "true":
                list_item.setProperty(hybrid.inputstreamname, 'inputstream.ffmpegdirect')
                list_item.setProperty('inputstream.ffmpegdirect.manifest_type', 'ts')
                list_item.setMimeType('video/mp2t')
                list_item.setContentLookup(False)
        else:
            stream_url = "http://127.0.0.1:6878/ace/manifest.m3u8?id=" + ace_id
            if getset.setting_get("UseInputStream") == "true":
                #list_item.setProperty(hybrid.inputstreamname, 'inputstream.adaptive')
                #list_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
                list_item.setProperty(hybrid.inputstreamname, 'inputstream.ffmpegdirect')
                list_item.setProperty('inputstream.ffmpegdirect.manifest_type', 'hls')
                list_item.setMimeType('application/vnd.apple.mpegurl')
                list_item.setContentLookup(False)

        #Play stream url
        xbmc.Player().play(stream_url, list_item, False)

        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Playing ace stream: " + ace_id, var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed playing ace stream", var.addonicon, 2500, False)

def run_server():
    try:
        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Running ace stream server", var.addonicon, 2500, False)

        #Get username
        userName = getpass.getuser()

        #Fix check if already running
        #Fix check operating system

        #Windows
        aceCommand = "start C:\\Users\\" + userName + "\\AppData\\Roaming\\ACEStream\\engine\\ace_engine.exe"
        runResult = os.system(aceCommand)

        #Linux RPI ARM docker
        aceCommand = "docker run -d -t -p 6878:6878 futebas/acestream-engine-arm:3.2.7.6"
        runResult = os.system(aceCommand)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed running ace stream server", var.addonicon, 2500, False)

if __name__ == "__main__":
    argumentDict = dict(hybrid.parse_qsl(sys.argv[2][1:]))
    if argumentDict:
        if argumentDict["action"] == "play":
            play_ace_stream(argumentDict["name"], argumentDict["id"])
        elif argumentDict["action"] == "add":
            add_history()
    else:
        func.check_user_folders()
        run_server()
        list_main()