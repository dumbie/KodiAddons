import xbmc
import cache
import func
import getset
import servicealarm
import servicecache
import serviceproxy
import var

#Service launch
if __name__ == '__main__':
    #Run Webbie Player on Kodi launch
    if getset.setting_get('RunAddonOnKodiLaunch') == 'true':
        func.run_addon()

    #Check if cache folder exists
    cache.cache_check_folder()

    #Start proxy server thread
    serviceproxy.start_proxy_server()

    #Start alarm check thread
    servicealarm.start_alarm_check()

    #Start cache clean thread
    servicecache.start_cache_clean()

    #Wait for service stop request
    while var.addonmonitor.abortRequested() == False:
        xbmc.sleep(100)

    #Stop proxy server thread
    serviceproxy.stop_proxy_server()

    #Stop alarm check thread
    servicealarm.stop_alarm_check()

    #Stop cache clean thread
    servicecache.stop_cache_clean()
