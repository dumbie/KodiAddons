import xbmcgui
import hybrid
import path
import var

def download_streams():
    try:
        DownloadHeaders = {
            "User-Agent": "Vogelspot"
        }
        DownloadRequest = hybrid.urllib_request(path.StreamsUrl, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadString = hybrid.string_decode_utf8(DownloadDataHttp.read())
        return DownloadString
    except:
        notificationIcon = path.addon('resources/skins/default/media/common/close.png')
        xbmcgui.Dialog().notification(var.addonname, 'Streams download failure.', notificationIcon, 2500, False)
        return None

def download_token(tokenUrl):
    try:
        DownloadHeaders = {
            "User-Agent": "Vogelspot"
        }
        DownloadRequest = hybrid.urllib_request(tokenUrl, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadString = hybrid.string_decode_utf8(DownloadDataHttp.read())
        return DownloadString
    except:
        notificationIcon = path.addon('resources/skins/default/media/common/close.png')
        xbmcgui.Dialog().notification(var.addonname, 'Token download failure.', notificationIcon, 2500, False)
        return None
