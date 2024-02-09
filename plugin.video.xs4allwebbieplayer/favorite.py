import json
import xbmcgui
import files
import path
import var

def favorite_television_json_load(forceLoad=False):
    try:
        if var.FavoriteTelevisionJson == [] or forceLoad == True:
            if files.existFile('FavoriteTelevision.js') == True:
                FavoriteJsonString = files.openFile('FavoriteTelevision.js')
                var.FavoriteTelevisionJson = json.loads(FavoriteJsonString)
    except:
        var.FavoriteTelevisionJson = []

def favorite_radio_json_load(forceLoad=False):
    try:
        if var.FavoriteRadioJson == [] or forceLoad == True:
            if files.existFile('FavoriteRadio.js') == True:
                FavoriteJsonString = files.openFile('FavoriteRadio.js')
                var.FavoriteRadioJson = json.loads(FavoriteJsonString)
    except:
        var.FavoriteRadioJson = []

def favorite_check(ChannelId, favoriteJsonFile):
    #Set Json target list variable
    if favoriteJsonFile == 'FavoriteTelevision.js':
        favoriteTargetJson = var.FavoriteTelevisionJson
    elif favoriteJsonFile == 'FavoriteRadio.js':
        favoriteTargetJson = var.FavoriteRadioJson
    return ChannelId in favoriteTargetJson

def favorite_toggle(listItem, favoriteJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Check current favorite status
    if favorite_check(ChannelId, favoriteJsonFile) == True:
        return favorite_remove(listItem, favoriteJsonFile)
    else:
        return favorite_add(listItem, favoriteJsonFile)

def favorite_add(listItem, favoriteJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    if favoriteJsonFile == 'FavoriteTelevision.js':
        favoriteTargetJson = var.FavoriteTelevisionJson
    elif favoriteJsonFile == 'FavoriteRadio.js':
        favoriteTargetJson = var.FavoriteRadioJson

    #Append the new favorite to Json
    favoriteTargetJson.append(ChannelId)

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(favoriteTargetJson).encode('ascii')
    files.saveFile(favoriteJsonFile, JsonDumpBytes)

    #Update the listitem status
    listItem.setProperty('ChannelFavorite', 'true')

    #Favorite has been set notification
    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender is gemarkeerd als favoriet.', notificationIcon, 2500, False)
    return 'Added'

def favorite_remove(listItem, favoriteJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    if favoriteJsonFile == 'FavoriteTelevision.js':
        favoriteTargetJson = var.FavoriteTelevisionJson
    elif favoriteJsonFile == 'FavoriteRadio.js':
        favoriteTargetJson = var.FavoriteRadioJson

    for favorite in favoriteTargetJson:
        try:
            if favorite == ChannelId:
                favoriteTargetJson.remove(favorite)
                break
        except:
            continue

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(favoriteTargetJson).encode('ascii')
    files.saveFile(favoriteJsonFile, JsonDumpBytes)

    #Update the listitem status
    listItem.setProperty('ChannelFavorite', 'false')

    #Favorite has been removed notification
    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender is ongemarkeerd als favoriet.', notificationIcon, 2500, False)
    return 'Removed'
