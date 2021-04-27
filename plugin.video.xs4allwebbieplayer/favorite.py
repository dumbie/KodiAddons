import json
import xbmc
import xbmcgui
import files
import func
import path
import var

def favorite_json_load():
    try:
        if files.existFile('FavoriteTelevision.js') == True:
            FavoriteTelevisionString = files.openFile('FavoriteTelevision.js')
            var.FavoriteTelevisionDataJson = json.loads(FavoriteTelevisionString)
    except:
        var.FavoriteTelevisionDataJson = []

def favorite_check(ChannelId):
    for favorite in var.FavoriteTelevisionDataJson:
        try:
            if favorite == ChannelId:
                return True
        except:
            continue
    return False

def favorite_add(listItem):
    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
    ChannelId = listItem.getProperty('ChannelId')

    #Check if favorite already exists
    if favorite_check(ChannelId) == True:
        return favorite_remove(listItem)

    #Append the new favorite to Json
    var.FavoriteTelevisionDataJson.append(ChannelId)

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(var.FavoriteTelevisionDataJson).encode('ascii')
    files.saveFile('FavoriteTelevision.js', JsonDumpBytes)

    #Update the listitem status
    listItem.setProperty('ChannelFavorite', 'true')

    #Favorite has been set notification
    xbmcgui.Dialog().notification(var.addonname, 'Zender is gemarkeerd als favoriet.', notificationIcon, 2500, False)
    return 'Added'

def favorite_remove(listItem):
    ChannelId = listItem.getProperty('ChannelId')

    for favorite in var.FavoriteTelevisionDataJson:
        try:
            if favorite == ChannelId:
                var.FavoriteTelevisionDataJson.remove(favorite)
                break
        except:
            continue

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(var.FavoriteTelevisionDataJson).encode('ascii')
    files.saveFile('FavoriteTelevision.js', JsonDumpBytes)

    #Update the listitem status
    listItem.setProperty('ChannelFavorite', 'false')

    #Favorite has been removed notification
    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender is ongemarkeerd als favoriet.', notificationIcon, 2500, False)
    return 'Removed'
