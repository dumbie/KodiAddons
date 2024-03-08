import xbmcgui
import apilogin
import dlfunc
import path
import var

def download(programName, forceUpdate=False):
    try:
        #Check if already cached in variables
        if var.SearchProgramDataJson != [] and forceUpdate == False:
            return True

        #Check if user needs to login
        if apilogin.ApiLogin(False) == False:
            notificationIcon = path.resources('resources/skins/default/media/common/search.png')
            xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt, niet aangemeld.', notificationIcon, 2500, False)
            return False

        #Download json data
        DownloadDataJson = dlfunc.download_gzip_json(path.program_search(programName))

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            if resultCode == 'KO':
                var.ApiLoggedIn(False)
                notificationIcon = path.resources('resources/skins/default/media/common/search.png')
                xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt: ' + resultMessage, notificationIcon, 2500, False)
                return False

        #Update variable cache
        var.SearchProgramDataJson = DownloadDataJson

        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/search.png')
        xbmcgui.Dialog().notification(var.addonname, 'Zoek download mislukt.', notificationIcon, 2500, False)
        return False
