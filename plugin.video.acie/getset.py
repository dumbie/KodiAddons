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
