import func
import xbmc
import servicealarm
import serviceproxy

#Service launch
if __name__ == '__main__':
    #Run Webbie Player on Kodi launch
    func.run_addon(False)

    #Start proxy server thread
    serviceproxy.start_proxy_server()

    #Start alarm check thread
    servicealarm.start_alarm_check()

    #Wait for service stop request
    addonmonitor = xbmc.Monitor()
    while addonmonitor.abortRequested() == False:
        xbmc.sleep(100)

    #Stop proxy server thread
    serviceproxy.stop_proxy_server()

    #Stop alarm check thread
    servicealarm.stop_alarm_check()
