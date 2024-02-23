import xbmcgui

def status_check_running():
    try:
        windowAddon = xbmcgui.Window(13000)
        addonStatus = windowAddon.getProperty('WebbiePlayerStatus')
        return addonStatus == 'Running'
    except:
        return False

def status_set(name, value):
    try:
        windowAddon = xbmcgui.Window(13000)
        windowAddon.setProperty('WebbiePlayer' + name, str(value))
        return True
    except:
        return False

def status_get(name):
    try:
        windowAddon = xbmcgui.Window(13000)
        return str(windowAddon.getProperty('WebbiePlayer' + name))
    except:
        return ''

def status_clear(name):
    try:
        windowAddon = xbmcgui.Window(13000)
        windowAddon.clearProperty('WebbiePlayer' + name)
        return True
    except:
        return False
