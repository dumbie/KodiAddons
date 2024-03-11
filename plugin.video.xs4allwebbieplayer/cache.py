from datetime import datetime, timedelta
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
        var.VodCacheDaysArray = []
        var.MoviesProgramDataJson = []
        var.MoviesVodDataJson = []
        var.SeriesProgramDataJson = []
        var.SeriesVodDataJson = []
        var.RecordingEventDataJson = []
        var.RecordingSeriesDataJson = []
        var.EpgCacheDaysArray = []
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

def cache_cleanup_days(fileName, epochCleanupTimeToday=0):
    try:
        fileRemoved = False
        dateStringToday = datetime.now().strftime('%Y-%m-%d')
        for cacheFile in files.listFiles(var.addonstoragecache):
            if cacheFile.startswith(fileName):
                dateStringFile = cacheFile.lstrip(fileName).rstrip('.js')
                dateTimeFile = func.datetime_from_string(dateStringFile, '%Y-%m-%d')
                daysPassed = func.day_offset_from_datetime(dateTimeFile)
                if daysPassed > var.VodDayOffsetPast:
                    cachePath = path.addonstoragecache(cacheFile)
                    if files.removeFile(cachePath) == True: fileRemoved = True
                elif epochCleanupTimeToday != 0 and dateStringFile == dateStringToday:
                    cachePath = path.addonstoragecache(cacheFile)
                    if cache_cleanup_file(cachePath, epochCleanupTimeToday) == True: fileRemoved = True
        return fileRemoved
    except:
        return False

def cache_cleanup_file(filePath, epochCleanupTime):
    try:
        timeCurrentEpoch = func.ticks_current_time()
        timeModifiedEpoch = files.fileTimeModifiedEpoch(filePath)
        timeDifferenceEpoch = timeCurrentEpoch - timeModifiedEpoch
        if timeDifferenceEpoch > epochCleanupTime:
            return files.removeFile(filePath)
        return False
    except:
        return False
