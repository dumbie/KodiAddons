import copy
import json
import xbmcgui
import dialog
import files
import func
import path
import var

def search_json_load():
    try:
        if files.existFile('SearchHistorySearch.js') == True:
            SearchHistorySearchString = files.openFile('SearchHistorySearch.js')
            var.SearchHistorySearchJson = json.loads(SearchHistorySearchString)
    except:
        var.SearchHistorySearchJson = []

def search_add(searchTerm):
    #Remove search term from Json
    search_remove(searchTerm, False)

    #Add search history to Json
    var.SearchHistorySearchJson.insert(0, searchTerm)

    #Trim search history length
    if len(var.SearchHistorySearchJson) > 30:
        var.SearchHistorySearchJson = var.SearchHistorySearchJson[:30]

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(var.SearchHistorySearchJson).encode('ascii')
    files.saveFile('SearchHistorySearch.js', JsonDumpBytes)

def search_remove(searchTerm, saveJson=True):
    #Remove search term from Json
    for search in var.SearchHistorySearchJson:
        try:
            if search == searchTerm:
                var.SearchHistorySearchJson.remove(search)
                break
        except:
            continue

    #Save the raw json data to storage
    if saveJson == True:
        JsonDumpBytes = json.dumps(var.SearchHistorySearchJson).encode('ascii')
        files.saveFile('SearchHistorySearch.js', JsonDumpBytes)

def search_dialog():
    #Check if search history is available
    if var.SearchHistorySearchJson == []:
        notificationIcon = path.resources('resources/skins/default/media/common/searchhistory.png')
        xbmcgui.Dialog().notification(var.addonname, 'Geen geschiedenis beschikbaar.', notificationIcon, 2500, False)
        return

    #Set search history
    dialogAnswers = var.SearchHistorySearchJson
    dialogHeader = 'Zoek geschiedenis'
    dialogSummary = 'Selecteer een eerder gebruikte zoek term.'
    dialogFooter = ''

    #Select search string
    searchString = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)

    #Check search string
    if searchString == 'DialogCancel':
        searchString = ''

    return searchString
