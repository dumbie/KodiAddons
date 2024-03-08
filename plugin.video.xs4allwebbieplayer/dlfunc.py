import gzip
import json
import getset
import hybrid
import var

def download_gzip_json(urlPath, sendData=None, sendMethod=None):
    try:
        downloadHeaders = {
            "User-Agent": getset.setting_get('CustomUserAgent'),
            "Cookie": var.ApiLoginCookie(),
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip'
        }

        #Create request
        downloadRequest = hybrid.urllib_request(urlPath, headers=downloadHeaders, data=sendData)
        if sendMethod != None:
            downloadRequest.get_method = lambda: sendMethod

        #Download information
        downloadDataHttp = hybrid.urllib_urlopen(downloadRequest)
        downloadDataInfo = downloadDataHttp.info()
        downloadDataEncoding = str(downloadDataInfo.get('Content-Encoding'))

        #Decode information
        if 'gzip' in downloadDataEncoding:
            gzipObject = hybrid.stringio_from_bytes(downloadDataHttp.read())
            gzipRead = gzip.GzipFile(fileobj=gzipObject)
            return json.load(gzipRead)
        else:
            return json.load(downloadDataHttp)
    except:
        return []
