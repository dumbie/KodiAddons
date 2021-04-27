import alarm
import func

#Service launch
if __name__ == '__main__':
    #Run Webbie Player on Kodi launch
    func.run_addon(False)

    #Check set program start alarms
    alarm.start_alarms_check()
