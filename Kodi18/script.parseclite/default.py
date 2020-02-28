import os
from datetime import datetime, timedelta
import main
import var
import xbmcgui

def check_script_permission():
    os_stat = os.stat(var.addonpath + '/scripts/script-run.sh')
    os.chmod(var.addonpath + '/scripts/script-run.sh', os_stat.st_mode | 111)

def check_multi_launch():
    if var.windowHome.getProperty('ParsecliteRunning'):
        lastrunSeconds = float(var.windowHome.getProperty('ParsecliteRunning'))
        currentSeconds = float((datetime.now() - datetime(1970,1,1)).total_seconds())
        if (currentSeconds - lastrunSeconds) <= 15:
            xbmcgui.Dialog().notification(var.addonname, 'Parsec Lite is already open.', var.addonicon, 2500, False)
            return False
        else:
            var.windowHome.setProperty('ParsecliteRunning', str(currentSeconds))
            return True
    else:
        currentSeconds = str((datetime.now() - datetime(1970,1,1)).total_seconds())
        var.windowHome.setProperty('ParsecliteRunning', currentSeconds)
        return True

def clear_home_variables():
    var.windowHome.clearProperty('ParsecliteRunning')

#Add-on launch
if __name__ == '__main__':
    allowLaunch = check_multi_launch()
    if allowLaunch:
        check_script_permission()
        main.switch_to_page()
