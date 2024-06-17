import xbmcgui
import dialog
import files
import func
import getset
import path
import var

def cache_check_folder():
    try:
        if files.existDirectory(var.addonstoragecache) == False:
            files.createDirectory(var.addonstoragecache)
        return True
    except:
        return False

def cache_reset_variables(jsonData):
    try:
        cleanedCacheFiles = jsonData.lstrip('["').rstrip('"]')
        cleanedCacheFiles = func.jsonstring_to_dictionary(cleanedCacheFiles)
        if any(x.startswith('epg') for x in cleanedCacheFiles):
            var.EpgCacheDaysArray = []
        if 'kidsprogram.js' in cleanedCacheFiles:
            var.KidsProgramDataJson = []
        if 'kidsvod.js' in cleanedCacheFiles:
            var.KidsVodDataJson = []
        if 'moviesprogram.js' in cleanedCacheFiles:
            var.MoviesProgramDataJson = []
        if 'moviesvod.js' in cleanedCacheFiles:
            var.MoviesVodDataJson = []
        if 'recordingevent.js' in cleanedCacheFiles:
            var.RecordingEventDataJson = []
        if 'recordingseries.js' in cleanedCacheFiles:
            var.RecordingSeriesDataJson = []
        if 'searchprogram.js' in cleanedCacheFiles:
            var.SearchProgramDataJson = []
        if 'seriesprogram.js' in cleanedCacheFiles:
            var.SeriesProgramDataJson = []
        if 'seriesvod.js' in cleanedCacheFiles:
            var.SeriesVodDataJson = []
        if 'sportprogram.js' in cleanedCacheFiles:
            var.SportProgramDataJson = []
        if 'stb.js' in cleanedCacheFiles:
            var.StbChannelsDataJson = []
        if 'web.js' in cleanedCacheFiles:
            var.WebChannelsDataJson = []
        return True
    except:
        return False

def cache_remove_all(showDialog=True, showNotification=True):
    try:
        if showDialog == True:
            cacheCleanTime = getset.setting_get('CacheCleanTimeOther')

            dialogAnswers = ['Handmatig vernieuwen']
            dialogHeader = 'Vernieuwen'
            dialogSummary = "Programma en opnames worden automatisch elke " + cacheCleanTime + " minuten vernieuwt bij het openen van een pagina, wilt u nu alles handmatig vernieuwen?"
            dialogFooter = ''

            dialogResult = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)
            if dialogResult != 'Handmatig vernieuwen':
                return

        #Reset cache variables 
        var.EpgCacheDaysArray = []
        var.KidsProgramDataJson = []
        var.KidsVodDataJson = []
        var.MoviesProgramDataJson = []
        var.MoviesVodDataJson = []
        var.RecordingEventDataJson = []
        var.RecordingSeriesDataJson = []
        var.SearchProgramDataJson = []
        var.SeriesProgramDataJson = []
        var.SeriesVodDataJson = []
        var.SportProgramDataJson = []
        var.StbChannelsDataJson = []
        var.WebChannelsDataJson = []

        #Remove cache files
        for cacheFile in files.listFiles(var.addonstoragecache):
            files.removeFile(path.addonstoragecache(cacheFile))

        if showNotification == True:
            xbmcgui.Dialog().notification(var.addonname, "Zender, programma en opnames worden vernieuwd.", var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, 'Cache bestanden verwijderen mislukt.', var.addonicon, 2500, False)
        return False

def cache_cleanup_files():
    cacheCleaned = []
    try:
        for cacheFile in files.listFiles(var.addonstoragecache):
            if cacheFile.startswith('epg'):
                if cache_cleanup_file(path.addonstoragecache(cacheFile), var.CacheCleanTimeEpg) == True: cacheCleaned.append(cacheFile)
            elif cacheFile == 'stb.js' or cacheFile == 'web.js':
                if cache_cleanup_file(path.addonstoragecache(cacheFile), var.CacheCleanTimeChannels) == True: cacheCleaned.append(cacheFile)
            else:
                if cache_cleanup_file(path.addonstoragecache(cacheFile), var.CacheCleanTimeOther()) == True: cacheCleaned.append(cacheFile)
        return cacheCleaned
    except:
        return cacheCleaned

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
