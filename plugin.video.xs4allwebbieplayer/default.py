import sys
import accent
import argument
import func
import getset
import main
import settings

def get_launch_type():
    try:
        str(sys.argv[0])
        str(sys.argv[1])
        str(sys.argv[2])
        return 'Source'
    except:
        return 'Script'

def launch_source():
    accent.change_addon_accent()
    if settings.check_login_settings() == False: return
    argument.set_launch_argument_source()
    argument.handle_launch_argument_source()

def launch_script():
    if func.check_addon_running() == False:
        accent.change_addon_accent()
        if settings.check_login_settings() == False: return
        func.stop_playing_media()
        settings.reset_global_variables()
        main.switch_to_page()
    else:
        func.open_window_id(getset.get_addon_windowId_top())

#Add-on launch
if __name__ == '__main__':
    launchType = get_launch_type()
    if launchType == 'Script':
        launch_script()
    else:
        launch_source()
