import xbmcgui
import files
import func
import path
import var

def cache_check_folder():
    try:
        if files.existDirectory(var.addonstoragecache) == False:
            files.createDirectory(var.addonstoragecache)
        return True
    except:
        return False

def cache_remove_all():
    try:
        cacheFiles = files.listFiles(var.addonstoragecache)
        for cacheFile in cacheFiles:
            files.removeFile(path.addonstoragecache(cacheFile))
        xbmcgui.Dialog().notification(var.addonname, "Zenders, programma's en opnames worden vernieuwd.", var.addonicon, 2500, False)
        return True
    except:
        xbmcgui.Dialog().notification(var.addonname, 'Cache bestanden verwijderen mislukt.', var.addonicon, 2500, False)
        return False

def cache_cleanup_all():
    try:
        #Check cache modified dates
        timeCleanupDaily = 1440 * 60
        timeCleanupMinutes = 15 * 60
        timeCurrentEpoch = func.ticks_current_time()
        cacheFiles = files.listFiles(var.addonstoragecache)
        for cacheFile in cacheFiles:
            cachePath = path.addonstoragecache(cacheFile)
            timeModifiedEpoch = files.fileTimeModifiedEpoch(cachePath)
            timeSinceModifiedEpoch = timeCurrentEpoch - timeModifiedEpoch
            if cacheFile.startswith('epg'):
                if cache_cleanup_check_epg(cacheFile) == True:
                    files.removeFile(cachePath)
            elif cacheFile.startswith('television') or cacheFile.startswith('radio'):
                if timeSinceModifiedEpoch > timeCleanupDaily:
                    files.removeFile(cachePath)
            else:
                if timeSinceModifiedEpoch > timeCleanupMinutes:
                    files.removeFile(cachePath)
        return True
    except:
        xbmcgui.Dialog().notification(var.addonname, 'Cache bestanden opruimen mislukt.', var.addonicon, 2500, False)
        return False

def cache_cleanup_check_epg(cacheFile):
    dateString = cacheFile.lstrip('epg').rstrip('.js')
    dateTimeFile = func.datetime_from_string(dateString, '%Y-%m-%d')
    passedDays = func.day_offset_from_datetime(dateTimeFile)
    return passedDays > var.VodDayOffsetPast
