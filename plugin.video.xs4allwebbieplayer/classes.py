#ExtAuth
class Class_ApiLogin_extAuth:
    def __init__(self, credentialsExtAuth=None):
        self.credentialsExtAuth = credentialsExtAuth

class Class_ApiLogin_credentialsExtAuth:
    def __init__(self, deviceInfo=None, credentials=None):
        self.deviceInfo = deviceInfo
        self.credentials = credentials
        self.remember = "Y"

class Class_ApiLogin_credentials:
    def __init__(self, username=None, password=None):
        self.loginType = "UsernamePassword"
        self.username = username
        self.password = password
        self.appId = "KPN"

class Class_ApiLogin_deviceInfo:
    def __init__(self, deviceId=None, deviceVendor=None, deviceModel=None, deviceFirmVersion=None, appVersion=None):
        self.deviceId = deviceId
        self.deviceIdType = "DEVICEID"
        self.deviceType = "PCTV"
        self.deviceVendor = deviceVendor
        self.deviceModel = deviceModel
        self.deviceFirmVersion = deviceFirmVersion
        self.appVersion = appVersion

#StdAuth
class Class_ApiLogin_stdAuth:
    def __init__(self, credentialsStdAuth=None):
        self.credentialsStdAuth = credentialsStdAuth

class Class_ApiLogin_credentialsStdAuth:
    def __init__(self, username=None, password=None, deviceRegistrationData=None):
        self.username = username
        self.password = password
        self.remember = "Y"
        self.deviceRegistrationData = deviceRegistrationData

class Class_ApiLogin_deviceRegistrationData:
    def __init__(self, deviceId=None, vendor=None, model=None, deviceFirmVersion=None, appVersion=None):
        self.deviceId = deviceId
        self.accountDeviceIdType = "DEVICEID"
        self.deviceType = "PCTV"
        self.vendor = vendor
        self.model = model
        self.deviceFirmVersion = deviceFirmVersion
        self.appVersion = appVersion

#Cache days
class Class_CacheDays:
    def __init__(self, dayDateString=None, dataJson=None):
        self.dayDateString = dayDateString
        self.dataJson = dataJson

#Search result
class Class_SearchResult:
    def __init__(self, cancelled=None, string=None):
        self.cancelled = cancelled
        self.string = string

#Convert class
def obj_to_dict(objx):
    dictx = {
        "__class__": objx.__class__.__name__,
        "__module__": objx.__module__
    }
    dictx.update(objx.__dict__)
    return dictx

def dict_to_obj(dictx):
    if "__class__" in dictx:
        class_name = dictx.pop("__class__")
        module_name = dictx.pop("__module__")
        module = __import__(module_name)
        classx = getattr(module,class_name)
        return classx(**dictx)
    else:
        return dictx
