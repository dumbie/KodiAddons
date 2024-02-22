import threading
import func
import var
import xbmc

class Class_ThreadSafe:
    #Initialize thread
    def __init__(self):
        self.allowed = False
        self.thread = None
        self.eventSleep = None
        self.threadName = ""

    #Start thread
    def Start(self, threadTarget, threadArgs=None, threadForce=False):
        try:
            #Check variables
            if self.thread != None:
                if threadForce == True:
                    xbmc.log("Thread is running, restarting: " + self.threadName, xbmc.LOGINFO)
                    self.Stop()
                else:
                    xbmc.log("Thread is running, stop it first: " + self.threadName, xbmc.LOGINFO)
                    return True

            #Set variables
            self.allowed = True
            self.threadName = str(threadTarget)
            self.eventSleep = threading.Event()
            if threadArgs == None:
                self.thread = threading.Thread(target=threadTarget)
            else:
                self.thread = threading.Thread(target=threadTarget, args=threadArgs)

            #Start thread in background
            self.thread.start()
            xbmc.log("Thread has started: " + self.threadName, xbmc.LOGINFO)
            return True
        except:
            xbmc.log("Thread failed to start.", xbmc.LOGINFO)
            return False

    #Stop thread
    def Stop(self):
        try:
            #Check variables
            if self.thread == None:
                xbmc.log("Thread not running, start it first.", xbmc.LOGINFO)
                return True

            #Stop thread looping
            self.allowed = False

            #Stop thread sleeping
            self.eventSleep.set()
            self.eventSleep.clear()

            #Wait for thread to have stopped
            if threading.current_thread() != self.thread:
                xbmc.log("Thread wait for stop: " + self.threadName, xbmc.LOGINFO)
                self.thread.join()
            xbmc.log("Thread has stopped: " + self.threadName, xbmc.LOGINFO)

            #Reset variables
            self.thread = None
            self.eventSleep = None
            self.threadName = ""
            return True
        except:
            xbmc.log("Thread failed to stop.", xbmc.LOGINFO)
            return False

    #Check if thread is running
    def Running(self):
        return self.thread != None

    #Check if thread is finished
    def Finished(self):
        return self.thread == None

    #Check if thread is allowed to run
    def Allowed(self, serviceThread=False):
        if serviceThread:
            return self.allowed and var.addonmonitor.abortRequested() == False
        else:
            return self.allowed and var.addonmonitor.abortRequested() == False and func.check_addon_running() == True

    #Sleep thread until set or timeout
    def Sleep(self, duration):
        self.eventSleep.wait(timeout=float(duration / 1000))
