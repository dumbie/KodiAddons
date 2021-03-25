from datetime import datetime, timedelta
import main
import var
import xbmcgui

def check_multi_launch():
    if var.windowHome.getProperty('VogelspotRunning'):
        lastrunSeconds = float(var.windowHome.getProperty('VogelspotRunning'))
        currentSeconds = float((datetime.now() - datetime(1970,1,1)).total_seconds())
        if (currentSeconds - lastrunSeconds) <= 15:
            xbmcgui.Dialog().notification(var.addonname, 'Vogelspot is already open.', var.addonicon, 2500, False)
            return False
        else:
            var.windowHome.setProperty('VogelspotRunning', str(currentSeconds))
            return True
    else:
        currentSeconds = str((datetime.now() - datetime(1970,1,1)).total_seconds())
        var.windowHome.setProperty('VogelspotRunning', currentSeconds)
        return True

def clear_home_variables():
    var.windowHome.clearProperty('VogelspotRunning')

#Add-on launch
if __name__ == '__main__':
    allowLaunch = check_multi_launch()
    if allowLaunch:
        main.switch_to_page()
