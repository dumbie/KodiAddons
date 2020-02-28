from datetime import datetime, timedelta
import main
import var
import xbmcgui

def check_multi_launch():
    if var.windowHome.getProperty('EnigmaStreamerRunning'):
        lastrunSeconds = float(var.windowHome.getProperty('EnigmaStreamerRunning'))
        currentSeconds = float((datetime.now() - datetime(1970,1,1)).total_seconds())
        if (currentSeconds - lastrunSeconds) <= 15:
            xbmcgui.Dialog().notification(var.addonname, 'Enigma streamer is already open.', var.addonicon, 2500, False)
            return False
        else:
            var.windowHome.setProperty('EnigmaStreamerRunning', str(currentSeconds))
            return True
    else:
        currentSeconds = str((datetime.now() - datetime(1970,1,1)).total_seconds())
        var.windowHome.setProperty('EnigmaStreamerRunning', currentSeconds)
        return True

def clear_home_variables():
    var.windowHome.clearProperty('EnigmaStreamerRunning')

#Add-on launch
if __name__ == '__main__':
    allowLaunch = check_multi_launch()
    if allowLaunch:
        main.switch_to_page()
