import ace
import json
import getset
import files
import func
import var
import xbmc
import xbmcgui

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

        #Play stream after adding
        if getset.setting_get("PlayAddStream") == "true":
            ace.play_ace_stream(ace_id, "", "")

        #Notification
        xbmcgui.Dialog().notification(var.addonname, "Added ace stream id", var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed adding ace stream id", var.addonicon, 2500, False)
