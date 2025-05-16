import os
from datetime import datetime, timedelta
import main
import var
import xbmcgui

def check_script_permission():
    set_script_permission(var.addonpath + '/scripts/moonlight-install.sh')
    set_script_permission(var.addonpath + '/scripts/moonlight-list.sh')
    set_script_permission(var.addonpath + '/scripts/moonlight-pair.sh')
    set_script_permission(var.addonpath + '/scripts/moonlight-stream.sh')

def set_script_permission(script_path):
    os_stat = os.stat(script_path)
    os.chmod(script_path, os_stat.st_mode | 111)

def check_multi_launch():
    if var.windowHome.getProperty('MoonliteRunning'):
        lastrunSeconds = float(var.windowHome.getProperty('MoonliteRunning'))
        currentSeconds = float((datetime.now() - datetime(1970,1,1)).total_seconds())
        if (currentSeconds - lastrunSeconds) <= 15:
            xbmcgui.Dialog().notification(var.addonname, 'Moonlite is already open.', var.addonicon, 2500, False)
            return False
        else:
            var.windowHome.setProperty('MoonliteRunning', str(currentSeconds))
            return True
    else:
        currentSeconds = str((datetime.now() - datetime(1970,1,1)).total_seconds())
        var.windowHome.setProperty('MoonliteRunning', currentSeconds)
        return True

def clear_home_variables():
    var.windowHome.clearProperty('MoonliteRunning')

#Add-on launch
if __name__ == '__main__':
    allowLaunch = check_multi_launch()
    if allowLaunch:
        check_script_permission()
        main.switch_to_page()
