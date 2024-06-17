import json
import xbmcgui
import files
import getset
import path
import var

def favorite_switch_mode(showNotification=False):
    #Switch favorites mode on or off
    if getset.setting_get('LoadChannelFavoritesOnly') == 'true':
        getset.setting_set('LoadChannelFavoritesOnly', 'false')
        if showNotification == True:
            notificationIcon = path.resources('resources/skins/default/media/common/star.png')
            xbmcgui.Dialog().notification(var.addonname, 'Toon alle zenders.', notificationIcon, 2500, False)
    else:
        getset.setting_set('LoadChannelFavoritesOnly', 'true')
        if showNotification == True:
            notificationIcon = path.resources('resources/skins/default/media/common/star.png')
            xbmcgui.Dialog().notification(var.addonname, 'Toon favorieten zenders.', notificationIcon, 2500, False)
    return True

def favorite_television_json_load(forceLoad=False):
    try:
        if var.FavoriteTelevisionJson == [] or forceLoad == True:
            if files.existFileUser('FavoriteTelevision.js') == True:
                FavoriteJsonString = files.openFileUser('FavoriteTelevision.js')
                var.FavoriteTelevisionJson = json.loads(FavoriteJsonString)
    except:
        var.FavoriteTelevisionJson = []

def favorite_radio_json_load(forceLoad=False):
    try:
        if var.FavoriteRadioJson == [] or forceLoad == True:
            if files.existFileUser('FavoriteRadio.js') == True:
                FavoriteJsonString = files.openFileUser('FavoriteRadio.js')
                var.FavoriteRadioJson = json.loads(FavoriteJsonString)
    except:
        var.FavoriteRadioJson = []

def favorite_target_variable(favoriteJsonFile):
    #Set Json target list variable
    if favoriteJsonFile == 'FavoriteTelevision.js':
        return var.FavoriteTelevisionJson
    elif favoriteJsonFile == 'FavoriteRadio.js':
        return var.FavoriteRadioJson

def favorite_check_channel(ChannelId, favoriteJsonFile):
    #Set Json target list variable
    favoriteTargetJson = favorite_target_variable(favoriteJsonFile)
    return ChannelId in favoriteTargetJson

def favorite_toggle_channel(listItem, favoriteJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Check current favorite status
    if favorite_check_channel(ChannelId, favoriteJsonFile) == True:
        return favorite_remove_channel(listItem, favoriteJsonFile)
    else:
        return favorite_add_channel(listItem, favoriteJsonFile)

def favorite_add_channel(listItem, favoriteJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    favoriteTargetJson = favorite_target_variable(favoriteJsonFile)

    #Append the new favorite to Json
    favoriteTargetJson.append(ChannelId)

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(favoriteTargetJson).encode('ascii')
    files.saveFileUser(favoriteJsonFile, JsonDumpBytes)

    #Update the listitem status
    listItem.setProperty('ChannelFavorite', 'true')

    #Favorite has been set notification
    notificationIcon = path.resources('resources/skins/default/media/common/star.png')
    xbmcgui.Dialog().notification(var.addonname, 'Zender is gemarkeerd als favoriet.', notificationIcon, 2500, False)
    return 'Added'

def favorite_remove_channel(listItem, favoriteJsonFile):
    #Get channel identifier
    ChannelId = listItem.getProperty('ChannelId')

    #Set Json target list variable
    favoriteTargetJson = favorite_target_variable(favoriteJsonFile)

    favoriteRemoved = False
    for favorite in favoriteTargetJson[:]:
        try:
            if favorite == ChannelId:
                favoriteTargetJson.remove(favorite)
                favoriteRemoved = True
        except:
            continue

    if favoriteRemoved == True:
        #Save the raw json data to storage
        JsonDumpBytes = json.dumps(favoriteTargetJson).encode('ascii')
        files.saveFileUser(favoriteJsonFile, JsonDumpBytes)

        #Update the listitem status
        listItem.setProperty('ChannelFavorite', 'false')

        #Favorite has been removed notification
        notificationIcon = path.resources('resources/skins/default/media/common/star.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zender is ongemarkeerd als favoriet.', notificationIcon, 2500, False)
    return 'Removed'
