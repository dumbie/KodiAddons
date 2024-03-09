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
    cache_reset_variables()
    cache_remove_files()

def cache_reset_variables():
    try:
        var.SearchProgramDataJson = []
        var.KidsProgramDataJson = []
        var.KidsVodDataJson = []
        var.SportProgramDataJson = []
        var.RadioChannelsDataJson = []
        var.TelevisionChannelsDataJson = []
        var.VodDayDataJson = []
        var.MoviesProgramDataJson = []
        var.MoviesVodDataJson = []
        var.SeriesProgramDataJson = []
        var.SeriesVodDataJson = []
        var.RecordingEventDataJson = []
        var.RecordingSeriesDataJson = []
        var.CacheEpgDaysArray = []
        return True
    except:
        return False

def cache_remove_file(cacheName):
    files.removeFile(path.addonstoragecache(cacheName))

def cache_remove_files():
    try:
        cacheFiles = files.listFiles(var.addonstoragecache)
        for cacheFile in cacheFiles:
            files.removeFile(path.addonstoragecache(cacheFile))
        xbmcgui.Dialog().notification(var.addonname, "Zender, programma en opnames worden vernieuwd.", var.addonicon, 2500, False)
        return True
    except:
        xbmcgui.Dialog().notification(var.addonname, 'Cache bestanden verwijderen mislukt.', var.addonicon, 2500, False)
        return False

def cache_cleanup_epg():
    try:
        fileRemoved = False
        for cacheFile in files.listFiles(var.addonstoragecache):
            if cacheFile.startswith('epg'):
                dateString = cacheFile.lstrip('epg').rstrip('.js')
                dateTimeFile = func.datetime_from_string(dateString, '%Y-%m-%d')
                daysPassed = func.day_offset_from_datetime(dateTimeFile)
                if daysPassed > var.VodDayOffsetPast:
                    fileRemoved = True
                    cachePath = path.addonstoragecache(cacheFile)
                    files.removeFile(cachePath)
                    xbmcgui.Dialog().notification(var.addonname, "Epg cache cleaned", var.addonicon, 2500, False)
        return fileRemoved
    except:
        return False

def cache_cleanup_file(filePath, epochCleanupTime):
    try:
        timeCurrentEpoch = func.ticks_current_time()
        timeModifiedEpoch = files.fileTimeModifiedEpoch(filePath)
        timeDifferenceEpoch = timeCurrentEpoch - timeModifiedEpoch
        if timeDifferenceEpoch > epochCleanupTime:
            xbmcgui.Dialog().notification(var.addonname, "File cache cleaned", var.addonicon, 2500, False)
            return files.removeFile(filePath)
        return False
    except:
        return False
