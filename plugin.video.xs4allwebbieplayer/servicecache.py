from datetime import datetime, timedelta
import xbmc
import cache
import func
import var

def thread_cache_clean():
    threadLastTime = ''
    while var.thread_cache_clean.Allowed(sleepDelayMs=1000):
        try:
            threadCurrentTime = datetime.now().strftime('%H:%M')
            if threadLastTime != threadCurrentTime:
                threadLastTime = threadCurrentTime
                cleanedCacheFiles = cache.cache_cleanup_files()
                if cleanedCacheFiles != []:
                    cleanedCacheFiles = '["' + func.dictionary_to_jsonstring(cleanedCacheFiles) + '"]'
                    xbmc.executebuiltin('NotifyAll(WebbiePlayer, cache_reset, ' + cleanedCacheFiles + ')')
        except:
            pass

def start_cache_clean():
    var.thread_cache_clean.Start(thread_cache_clean)

def stop_cache_clean():
    var.thread_cache_clean.Stop()
