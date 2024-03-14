import xbmc
import threadclass

#Add-on variables
addonmonitor = xbmc.Monitor()

#Service - Alarm variables
thread_alarm_timer = threadclass.Class_ThreadSafe()

#Service - Cache variables
thread_cache_cleanup = threadclass.Class_ThreadSafe()

#Service - Proxy variables
ProxyServer = None
thread_proxy_server = threadclass.Class_ThreadSafe()
