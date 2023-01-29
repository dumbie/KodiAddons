import json
import random
import re
from datetime import datetime, timedelta
from threading import Thread
import xbmc
import xbmcgui
import alarm
import classes
import default
import dialog
import download
import func
import hybrid
import path
import television
import var
import zap

def ApiGenerateDeviceId():
    if var.addon.getSetting('LoginDeviceId120') == '':
        DeviceId = ''
        CurrentTime = str(datetime.utcnow())
        random.seed(CurrentTime)
        for _ in range(64):
            DeviceId += str(random.randint(0,9))

        #Update the settings
        var.addon.setSetting('LoginDeviceId120', DeviceId)

def thread_login_auto():
    while var.thread_login_auto != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True:
        #Check if it is time to auto login
        LastLoginSeconds = int((datetime.now() - var.ApiLastLogin).total_seconds())
        if LastLoginSeconds >= 890:
            if var.ApiLoggedIn == True:
                ApiLogin(False)
        else:
            xbmc.sleep(5000)

def ApiSetEndpointAdresNumber():
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Content-Type": "application/json"
        }

        DownloadRequest = hybrid.urllib_request(path.api_endpoint_number(), headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        var.ApiEndpointUrl = str(DownloadDataJson['result']['url'])
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Mislukt om api adres te downloaden.', notificationIcon, 2500, False)
        return False

def ApiSetEndpointAdresEmail():
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Content-Type": "application/json"
        }
        
        apiEndpoint = classes.Class_ApiEndpoint()
        apiEndpoint.username = var.addon.getSetting('LoginEmail')
        apiEndpoint.password = var.addon.getSetting('LoginPasswordEmail')
        apiEndpoint = apiEndpoint.__dict__

        DownloadData = json.dumps(apiEndpoint).encode('ascii')
        DownloadRequest = hybrid.urllib_request(path.api_endpoint_email(), data=DownloadData, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)

        var.ApiEndpointUrl = str(DownloadDataJson['result']['url'])
        return True
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Mislukt om api adres te downloaden.', notificationIcon, 2500, False)
        return False

def ApiLogin(LoginNotification=False):
    #Check login retry limit
    if var.ApiLoginCount > 2:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Aanmeld poging limiet bereikt, herstart de add-on.', notificationIcon, 2500, False)
        return False
    else:
        var.ApiLoginCount += 1

    #Generate the device id
    ApiGenerateDeviceId()

    #Check login settings
    default.check_login_settings()

    #Check the login type
    if var.addon.getSetting('LoginType') == 'Abonnementsnummer':
        #Download and set api endpoint adres
        ApiSetEndpointAdresNumber()

        loginDevice = classes.Class_ApiLogin_deviceRegistrationData()
        loginDevice.deviceId = var.addon.getSetting('LoginDeviceId120')
        loginDevice.vendor = "Webbie Player"
        loginDevice.model = str(var.addonversion)
        loginDevice.deviceFirmVersion = "Kodi"
        loginDevice.appVersion = str(var.kodiversion)
        loginDevice = loginDevice.__dict__

        loginAuth = classes.Class_ApiLogin_credentialsStdAuth()
        loginAuth.username = var.addon.getSetting('LoginUsername')
        loginAuth.password = var.addon.getSetting('LoginPassword')
        loginAuth.deviceRegistrationData = loginDevice
        loginAuth = loginAuth.__dict__

        loginData = classes.Class_ApiLogin_stdAuth()
        loginData.credentialsStdAuth = loginAuth
        loginData = loginData.__dict__
    else:
        #Download and set api endpoint adres
        ApiSetEndpointAdresEmail()

        loginDevice = classes.Class_ApiLogin_deviceInfo()
        loginDevice.deviceId = var.addon.getSetting('LoginDeviceId120')
        loginDevice.deviceVendor = "Webbie Player"
        loginDevice.deviceModel = str(var.addonversion)
        loginDevice.deviceFirmVersion = "Kodi"
        loginDevice.appVersion = str(var.kodiversion)
        loginDevice = loginDevice.__dict__

        loginCredentials = classes.Class_ApiLogin_credentials()
        loginCredentials.username = var.addon.getSetting('LoginEmail')
        loginCredentials.password = var.addon.getSetting('LoginPasswordEmail')
        loginCredentials = loginCredentials.__dict__

        loginAuth = classes.Class_ApiLogin_credentialsExtAuth()
        loginAuth.deviceInfo = loginDevice
        loginAuth.credentials = loginCredentials
        loginAuth = loginAuth.__dict__

        loginData = classes.Class_ApiLogin_extAuth()
        loginData.credentialsExtAuth = loginAuth
        loginData = loginData.__dict__

    #Request login by sending data
    try:
        DownloadHeaders = {
            "User-Agent": var.addon.getSetting('CustomUserAgent'),
            "Content-Type": "application/json"
        }

        DownloadData = json.dumps(loginData).encode('ascii')
        DownloadRequest = hybrid.urllib_request(path.api_login(), data=DownloadData, headers=DownloadHeaders)
        DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
        DownloadDataJson = json.load(DownloadDataHttp)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, 'Aanmelden is mislukt.', notificationIcon, 2500, False)
        var.ApiLoggedIn = False
        var.ApiLastLogin = datetime(1970, 1, 1)
        var.ApiLoginCookie = ''
        var.ApiLoginToken = ''
        return False

    #Check if connection is successful
    if DownloadDataJson['resultCode'] and DownloadDataJson['errorDescription']:
        resultCode = DownloadDataJson['resultCode']
        resultMessage = DownloadDataJson['message']
        errorDescription = DownloadDataJson['errorDescription']
        if errorDescription == '403-3161':
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Inloggen 24 uur geblokkeerd.', notificationIcon, 2500, False)
            var.ApiLoggedIn = False
            var.ApiLastLogin = datetime(1970, 1, 1)
            var.ApiLoginCookie = ''
            var.ApiLoginToken = ''
            return False
        elif errorDescription == '401-3035':
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Uw account is (tijdelijk) geblokkeerd.', notificationIcon, 2500, False)
            var.ApiLoggedIn = False
            var.ApiLastLogin = datetime(1970, 1, 1)
            var.ApiLoginCookie = ''
            var.ApiLoginToken = ''
            return False
        elif resultCode == 'KO':
            notificationIcon = path.resources('resources/skins/default/media/common/error.png')
            xbmcgui.Dialog().notification(var.addonname, 'Onjuiste gegevens: ' + resultMessage, notificationIcon, 5000, False)
            var.ApiLoggedIn = False
            var.ApiLastLogin = datetime(1970, 1, 1)
            var.ApiLoginCookie = ''
            var.ApiLoginToken = ''
            return False

    #Read and set the returned token
    var.ApiLoginToken = hybrid.urllib_getheader(DownloadDataHttp, 'X-Xsrf-Token')

    #Filter and clone the cookie contents
    HeaderCookie = hybrid.urllib_getheader(DownloadDataHttp, 'Set-Cookie')
    
    var.ApiLoginCookie = ''
    cookie_split = re.findall(r"([^\s]*?=.*?(?=;|,|$))", HeaderCookie)
    for cookie in cookie_split:
        if cookie.startswith('Path') == False and cookie.startswith('Expires') == False and cookie.startswith('Max-Age') == False:
            var.ApiLoginCookie += cookie + ';'
    var.ApiLoginCookie = var.ApiLoginCookie[:-1]

    #Show the login notification
    if LoginNotification == True:
        xbmcgui.Dialog().notification(var.addonname, 'Aangemeld, veel kijkplezier.', var.addonicon, 2500, False)

    #Check if user has home access
    ApiCheckHomeAccess(DownloadDataJson)

    #Update api login variables
    var.ApiLoginCount = 0
    var.ApiLoggedIn = True
    var.ApiLastLogin = datetime.now()

    #Start the auto login thread
    if var.thread_login_auto == None:
        var.thread_login_auto = Thread(target=thread_login_auto)
        var.thread_login_auto.start()

    return True

def ApiCheckHomeAccess(DownloadDataJson):
    try:
        if bool(DownloadDataJson['resultObj']['profile']['sessionProfileData']['isOutOfHome']):
            var.windowHome.setProperty('WebbiePlayerHomeAccess', 'False')
            var.ApiHomeAccess = False
            return False
        else:
            var.windowHome.setProperty('WebbiePlayerHomeAccess', 'True')
            var.ApiHomeAccess = True
            return True
    except:
        return True