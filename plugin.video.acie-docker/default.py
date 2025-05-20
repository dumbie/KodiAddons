import sys
import getset
import history
import ace
import server
import func
import var
import hybrid
import xbmcgui
import xbmcplugin

def list_main():
    try:
        #Clean and load json history
        history.load_history()

        #Set launch handle
        LaunchHandle = int(sys.argv[1])

        #Set icon paths
        iconAdd = func.path_addon('resources/add.png')
        iconInfo = func.path_addon('resources/info.png')

        #Add default items
        if getset.setting_get("PlayAddStream") == "true":
            list_label = "Add and play ace stream id"
        else:
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
                ace_title = "Unknown"
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

if __name__ == "__main__":
    argumentDict = dict(hybrid.parse_qsl(sys.argv[2][1:]))
    if argumentDict:
        if argumentDict["action"] == "play":
            ace.play_ace_stream(argumentDict["id"], argumentDict["icon"], argumentDict["title"])
        elif argumentDict["action"] == "add":
            history.add_history()
        elif argumentDict["action"] == "info":
            ace.show_info_ace_stream()
        elif argumentDict["action"] == "remove":
            history.remove_history(argumentDict["id"])
    else:
        #Check user folders
        func.check_user_folders()

        #Run ace stream server
        server.run_server()

        #List main menu
        list_main()