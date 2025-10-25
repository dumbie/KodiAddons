import subprocess
import platform
import struct
import var
import getpass
import getset
import xbmc
import xbmcgui
import console
import time

def run_server():
    try:
        #Check if started
        if getset.global_get("AceRunning") == 'true':
            return
        else:
            getset.global_set("AceRunning", 'true')

        #Get username
        userName = getpass.getuser()

        #Apple IOS
        if xbmc.getCondVisibility('System.Platform.IOS'):
            #Show and update console
            console.console_show('Run ace stream server', 'Operating system not supported.')

        #Apple OSX
        if xbmc.getCondVisibility('System.Platform.OSX'):
            #Show and update console
            console.console_show('Run ace stream server', 'Operating system not supported.')

        #Android
        if xbmc.getCondVisibility('System.Platform.Android'):
            #Show and update console
            console.console_show('Run ace stream server', 'Running ace stream server, please wait.')

            #Launch ace stream server
            #Fix find way to avoid error message
            runCommand = 'StartAndroidActivity("","org.acestream.action.start_content","","")'
            process = xbmc.executebuiltin(runCommand)

            #Check result
            if process == 0:
                console.console_show('Run ace stream server', "Ace stream server is running")
            else:
                console.console_show('Run ace stream server', "Failed to run ace stream server")

        #Windows
        if xbmc.getCondVisibility('System.Platform.Windows'):
            #Show and update console
            console.console_show('Run ace stream server', 'Running ace stream server, please wait.')

            #Launch ace stream server
            runCommand = "C:\\Users\\" + userName + "\\AppData\\Roaming\\ACEStream\\engine\\ace_engine.exe"
            process = subprocess.Popen(runCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            #Check process return code
            if process.returncode is None:
                console.console_show('Run ace stream server', "Ace stream server is running")
            else:
                console.console_show('Run ace stream server', "Failed to run ace stream server")

        #Linux Docker
        if xbmc.getCondVisibility('System.Platform.Linux'):
            #Check system processor architecture
            runArchitecture = ''
            systemArchitecture = platform.machine().lower()
            system32Mode = struct.calcsize('P') * 8 == 32
            if ('arm' in systemArchitecture or 'aarch' in systemArchitecture) and system32Mode == False:
                runArchitecture = 'arm64'
            elif 'arm' in systemArchitecture or 'aarch' in systemArchitecture:
                runArchitecture = 'arm32'
            else:
                runArchitecture = 'x64'

            #Launch ace stream server
            runCommand = "docker run --detach --publish 6878:6878 jopsis/acestream:" + runArchitecture
            process = subprocess.Popen(runCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

            #Show and update console
            console.console_process_poll(process, 'Run ace stream server')

            #Wait for completion
            process.wait()

        #Close console
        time.sleep(3)
        console.console_close()
    except:
       xbmcgui.Dialog().notification(var.addonname, "Failed running ace stream server", var.addonicon, 2500, False)
