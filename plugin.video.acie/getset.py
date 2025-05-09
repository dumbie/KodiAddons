import xbmcaddon
import var

#Addon settings
def setting_set(setName, setObject):
    try:
        var.addon.setSetting(setName, setObject)
        return True
    except:
        return False

def setting_get(setName, reloadSettings=False):
    try:
        if reloadSettings == True:
            var.addon = xbmcaddon.Addon()
        return var.addon.getSetting(setName)
    except:
        return ''

#Global properties
def global_clear(propName):
    try:
        var.windowHome.clearProperty('Acie' + propName)
        return True
    except:
        return False

def global_set(propName, propValue):
    try:
        var.windowHome.setProperty('Acie' + propName, propValue)
        return True
    except:
        return False

def global_get(propName):
    try:
        return var.windowHome.getProperty('Acie' + propName)
    except:
        return ''