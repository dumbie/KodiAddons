import xbmcaddon
import xbmcgui
import func
import var

#Addon status
def check_addon_running():
    windowId = var.WINDOW_ADDON
    for _ in range(5):
        try:
            if str(xbmcgui.Window(windowId).getProperty('WebbiePlayerStatus')) == 'Running':
                return True
        except:
            pass
        windowId += 1
    return False

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

#Addon properties
def addon_clear(propName):
    try:
        var.guiMain.clearProperty('WebbiePlayer' + propName)
        return True
    except:
        return False

def addon_set(propName, propValue):
    try:
        var.guiMain.setProperty('WebbiePlayer' + propName, propValue)
        return True
    except:
        return False

def addon_get(propName):
    try:
        return var.guiMain.getProperty('WebbiePlayer' + propName)
    except:
        return ''

#Global properties
def global_clear(propName):
    try:
        var.windowHome.clearProperty('WebbiePlayer' + propName)
        return True
    except:
        return False

def global_set(propName, propValue):
    try:
        var.windowHome.setProperty('WebbiePlayer' + propName, propValue)
        return True
    except:
        return False

def global_get(propName):
    try:
        return var.windowHome.getProperty('WebbiePlayer' + propName)
    except:
        return ''

def global_pickle_get(varName, defaultObject=None):
    try:
        pickleString = global_get(varName)
        return func.picklestring_to_object(pickleString)
    except:
        return defaultObject

def global_pickle_set(varName, varObject):
    try:
        pickleString = func.object_to_picklestring(varObject)
        global_set(varName, pickleString)
        return True
    except:
        return False
