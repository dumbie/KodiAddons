from threading import Thread
import var
import func
import xbmc

#Start thread with wait
def start_safe_thread(threadName, threadTarget):
    #Stop previous thread and wait
    threadVariable = getattr(var, threadName)
    if threadVariable != None:
        setattr(var, threadName, None)
        xbmc.sleep(500) #Improve: wait for thread to finish

    #Start task in new thread
    threadVariable = Thread(target=threadTarget)
    threadVariable.start()
    setattr(var, threadName, threadVariable)

#Stop and reset all threads
def stop_reset_threads():
    var.thread_check_requirements = None
    var.thread_zap_wait_timer = None
    var.thread_channel_delay_timer = None
    var.thread_update_television_program = None
    var.thread_update_epg_program = None
    var.thread_update_epg_channel = None
    var.thread_update_playergui_info = None
    var.thread_hide_playergui_info = None
    var.thread_sleep_timer = None
    var.thread_login_auto = None

#Check if thread loop is allowed
def loop_allowed_addon(threadVariable):
    return threadVariable != None and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True

#Check if thread loop is allowed
def loop_allowed_service(threadVariable):
    return threadVariable != None and var.addonmonitor.abortRequested() == False
