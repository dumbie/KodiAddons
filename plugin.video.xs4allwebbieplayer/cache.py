from datetime import datetime
import xbmcgui
import dialog
import files
import func
import path
import var
import getset

def cache_check_folder():
    try:
        if files.existDirectory(var.addonstoragecache) == False:
            files.createDirectory(var.addonstoragecache)
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

        #Remove cache files
        cacheFiles = files.listFiles(var.addonstoragecache)
        for cacheFile in cacheFiles:
            files.removeFile(path.addonstoragecache(cacheFile))

        if showNotification == True:
            xbmcgui.Dialog().notification(var.addonname, "Zender, programma en opnames worden vernieuwd.", var.addonicon, 2500, False)
    except:
        xbmcgui.Dialog().notification(var.addonname, 'Cache bestanden verwijderen mislukt.', var.addonicon, 2500, False)
        return False

def cache_cleanup_files(fileName, epochCleanupTime):
    try:
        fileRemoved = False
        for cacheFile in files.listFiles(var.addonstoragecache):
            if cacheFile.startswith(fileName):
                cachePath = path.addonstoragecache(cacheFile)
                if cache_cleanup_file(cachePath, epochCleanupTime) == True: fileRemoved = True
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
