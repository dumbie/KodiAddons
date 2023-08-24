import classes
import func
import hybrid
import json
import xbmc
import dialog
import files
import var

def search_history_json_load():
    try:
        if var.SearchHistorySearchJson == [] and files.existFile('SearchHistorySearch.js') == True:
            SearchHistorySearchString = files.openFile('SearchHistorySearch.js')
            var.SearchHistorySearchJson = json.loads(SearchHistorySearchString)
    except:
        var.SearchHistorySearchJson = []

def search_history_add(searchTerm):
    #Check search term
    if func.string_isnullorempty(searchTerm) == True:
        return

    #Remove search term from Json
    search_history_remove(searchTerm, False)

    #Add search history to Json
    var.SearchHistorySearchJson.insert(0, searchTerm)

    #Trim search history length
    if len(var.SearchHistorySearchJson) > 40:
        var.SearchHistorySearchJson = var.SearchHistorySearchJson[:40]

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(var.SearchHistorySearchJson).encode('ascii')
    files.saveFile('SearchHistorySearch.js', JsonDumpBytes)

def search_history_remove(searchTerm, saveJson=True):
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

def search_dialog(headerText='Zoeken'):
    #Load search history
    search_history_json_load()

    #Set search history
    dialogAnswers = hybrid.deep_copy_list(var.SearchHistorySearchJson)
    dialogAnswers.insert(0, '- Nieuw zoek term gebruiken')

    dialogHeader = headerText
    dialogSummary = 'Selecteer een eerder gebruikte zoek term of klik op nieuw zoek term.'
    dialogFooter = ''

    #Select search string
    searchString = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)

    #Check search string
    if searchString == '- Nieuw zoek term gebruiken':
        keyboard = xbmc.Keyboard('default', 'heading')
        keyboard.setHeading(headerText)
        keyboard.setDefault('')
        keyboard.setHiddenInput(False)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            #Get keyboard text
            keyboardText = keyboard.getText()

            #Add search history to Json
            search_history_add(keyboardText)

            #Return search result
            searchResult = classes.Class_SearchResult()
            searchResult.cancelled = False
            searchResult.string = keyboardText
            return searchResult
        else:
            #Return search result
            searchResult = classes.Class_SearchResult()
            searchResult.cancelled = True
            searchResult.string = ''
            return searchResult
    elif searchString == 'DialogCancel':
        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = True
        searchResult.string = ''
        return searchResult
    else:
        #Add search history to Json
        search_history_add(searchString)

        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = searchString
        return searchResult
