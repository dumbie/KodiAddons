import alarm
import func
import proxy

#Service launch
if __name__ == '__main__':
    #Run Webbie Player on Kodi launch
    func.run_addon(False)

    #Start localhost proxy server
    proxy.start_proxy_server()

    #Check set program start alarms
    alarm.start_alarms_check()
