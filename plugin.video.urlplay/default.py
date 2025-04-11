import xbmc
import xbmcgui
import json
import func
import var

def play_url():
    try:
        #Show keyboard
        keyboard = xbmc.Keyboard("default", "heading")
        keyboard.setHeading("Play URL")
        keyboard.setDefault("")
        keyboard.setHiddenInput(False)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            open_url = keyboard.getText()
        else:
            open_url = ""

        #Check empty
        if func.string_isnullorempty(open_url) == True:
            xbmcgui.Dialog().notification(var.addonname, "Empty playing url", var.addonicon, 2500, False)
            return

        #Convert json rpc to string
        jsonRpcDictionary = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'Player.Open',
            'params':
            {
                "item":
                {
                    "file": "plugin://plugin.video.sendtokodi/?" + open_url
                }
            }
        }

        #Execute json rpc
        xbmc.executeJSONRPC(json.dumps(jsonRpcDictionary))
    except:
        xbmcgui.Dialog().notification(var.addonname, "Failed playing url", var.addonicon, 2500, False)

if __name__ == "__main__":
    play_url()