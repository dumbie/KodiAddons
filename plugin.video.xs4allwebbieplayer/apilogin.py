from datetime import datetime, timedelta
import json
import random
import re
import xbmcgui
import classes
import dlfunc
import func
import getset
import hybrid
import path
import var

def ApiGenerateDeviceId():
    try:
        if func.string_isnullorempty(getset.setting_get('LoginDeviceId120')) == True:
            DeviceId = ''
            CurrentTimeUtc = str(datetime.utcnow())
            random.seed(CurrentTimeUtc)
            for _ in range(64):
                DeviceId += str(random.randint(0,9))

            #Update api login settings
            getset.setting_set('LoginDeviceId120', DeviceId)
        return True
    except:
        return False

def ApiSetEndpoint():
    try:
        DownloadDataJson = dlfunc.download_gzip_json(path.api_endpoint())
        var.ApiEndpointUrl(str(DownloadDataJson['result']['url']))
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Mislukt om api adres te downloaden.', notificationIcon, 2500, False)
        return False

def ApiCheckHomeAccess(DownloadDataJson):
    try:
        if bool(DownloadDataJson['resultObj']['profile']['sessionProfileData']['isOutOfHome']):
            var.windowHome.setProperty('WebbiePlayerHomeAccess', 'False')
            var.ApiHomeAccess(False)
            return False
        else:
            var.windowHome.setProperty('WebbiePlayerHomeAccess', 'True')
            var.ApiHomeAccess(True)
            return True
    except:
        return True

def ApiFailVariableUpdate():
    try:
        var.ApiLoggedIn(False)
        var.ApiLoginLastDateTime(datetime(1970,1,1))
        var.ApiLoginLastUsername('')
        var.ApiLoginCookie('')
        newFailCount = var.ApiLoginFailCount() + 1
        var.ApiLoginFailCount(newFailCount)
        return True
    except:
        return False

def ApiLogin(showNotification=False, forceLogin=False):
    try:
        #Check failed login retry limit
        if var.ApiLoginFailCount() > 2:
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Aanmeld poging limiet bereikt, herstart Kodi.', notificationIcon, 2500, False)
            return False

        #Check if login cookie has expired
        loginCookieExpired = int((datetime.now() - var.ApiLoginLastDateTime()).total_seconds()) > 890

        #Check if login username changed
        if getset.setting_get('LoginType') == 'Abonnementsnummer':
            loginUsername = getset.setting_get('LoginUsername')
        else:
            loginUsername = getset.setting_get('LoginEmail')
        loginUsernameChanged = loginUsername != var.ApiLoginLastUsername()

        #Check if login is needed
        if forceLogin == False and var.ApiLoggedIn() == True and loginCookieExpired == False and loginUsernameChanged == False:
            return True

        #Generate device id
        ApiGenerateDeviceId()

        #Download and set api endpoint adres
        ApiSetEndpoint()

        #Check the login type
        if getset.setting_get('LoginType') == 'Abonnementsnummer':
            loginDevice = classes.Class_ApiLogin_deviceRegistrationData()
            loginDevice.deviceId = getset.setting_get('LoginDeviceId120')
            loginDevice.vendor = "Webbie Player"
            loginDevice.model = str(var.addonversion)
            loginDevice.deviceFirmVersion = "Kodi"
            loginDevice.appVersion = str(var.kodiversion)
            loginDevice = loginDevice.__dict__

            loginAuth = classes.Class_ApiLogin_credentialsStdAuth()
            loginAuth.username = loginUsername
            loginAuth.password = getset.setting_get('LoginPassword')
            loginAuth.deviceRegistrationData = loginDevice
            loginAuth = loginAuth.__dict__

            loginData = classes.Class_ApiLogin_stdAuth()
            loginData.credentialsStdAuth = loginAuth
            loginData = loginData.__dict__
        else:
            loginDevice = classes.Class_ApiLogin_deviceInfo()
            loginDevice.deviceId = getset.setting_get('LoginDeviceId120')
            loginDevice.deviceVendor = "Webbie Player"
            loginDevice.deviceModel = str(var.addonversion)
            loginDevice.deviceFirmVersion = "Kodi"
            loginDevice.appVersion = str(var.kodiversion)
            loginDevice = loginDevice.__dict__

            loginCredentials = classes.Class_ApiLogin_credentials()
            loginCredentials.username = loginUsername
            loginCredentials.password = getset.setting_get('LoginPasswordEmail')
            loginCredentials = loginCredentials.__dict__

            loginAuth = classes.Class_ApiLogin_credentialsExtAuth()
            loginAuth.deviceInfo = loginDevice
            loginAuth.credentials = loginCredentials
            loginAuth = loginAuth.__dict__

            loginData = classes.Class_ApiLogin_extAuth()
            loginData.credentialsExtAuth = loginAuth
            loginData = loginData.__dict__

        #Request login by sending data
        DownloadHeaders = {
            "User-Agent": getset.setting_get('CustomUserAgent'),
            "Content-Type": "application/json"
        }

        DownloadDataSend = json.dumps(loginData).encode('ascii')
        DownloadRequest = hybrid.urllib_request(path.api_login(), data=DownloadDataSend, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        #Check if connection is successful
        if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
            resultCode = DownloadDataJson['resultCode']
            resultMessage = DownloadDataJson['message']
            errorDescription = DownloadDataJson['errorDescription']
            if errorDescription == '403-3161':
                notificationIcon = path.resources('resources/skins/default/media/common/error.png')
                xbmcgui.Dialog().notification(var.addonname, 'Inloggen 24 uur geblokkeerd.', notificationIcon, 2500, False)
                ApiFailVariableUpdate()
                return False
            elif errorDescription == '401-3035':
                notificationIcon = path.resources('resources/skins/default/media/common/error.png')
                xbmcgui.Dialog().notification(var.addonname, 'Uw account is (tijdelijk) geblokkeerd.', notificationIcon, 2500, False)
                ApiFailVariableUpdate()
                return False
            elif resultCode == 'KO':
                notificationIcon = path.resources('resources/skins/default/media/common/error.png')
                xbmcgui.Dialog().notification(var.addonname, 'Onjuiste gegevens: ' + resultMessage, notificationIcon, 5000, False)
                ApiFailVariableUpdate()
                return False

        #Filter cookie contents
        newApiLoginCookie = ''
        HeaderCookie = hybrid.urllib_getheader(DownloadDataHttp, 'Set-Cookie')
        try:
            cookie_split = re.findall(r"([^\s]*?=.*?(?=;|,|$))", HeaderCookie)
            for cookie in cookie_split:
                if cookie.startswith('Path') == False and cookie.startswith('Expires') == False and cookie.startswith('Max-Age') == False:
                    newApiLoginCookie += cookie + ';'
            newApiLoginCookie = newApiLoginCookie[:-1]
        except:
            pass

        #Check cookie contents
        if func.string_isnullorempty(newApiLoginCookie) == True:
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Login cookie lezen mislukt.', notificationIcon, 2500, False)
            ApiFailVariableUpdate()
            return False
        else:
            var.ApiLoginCookie(newApiLoginCookie)

        #Check if user has home access
        ApiCheckHomeAccess(DownloadDataJson)

        #Update api login variables
        var.ApiLoggedIn(True)
        var.ApiLoginLastDateTime(datetime.now())
        var.ApiLoginLastUsername(loginUsername)
        var.ApiLoginFailCount(0)

        #Update api login settings
        getset.setting_set('LoginChecked', 'true')

        #Show login notification
        if showNotification == True:
            xbmcgui.Dialog().notification(var.addonname, 'Aangemeld, veel kijkplezier.', var.addonicon, 2500, False)
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Aanmelden mislukt, probeer het nog een keer.', notificationIcon, 2500, False)
        ApiFailVariableUpdate()
        return False
