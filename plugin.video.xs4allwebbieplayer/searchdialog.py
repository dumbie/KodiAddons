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
        if var.SearchHistoryProgramJson == [] and files.existFile('SearchHistorySearch.js') == True:
            SearchHistorySearchString = files.openFile('SearchHistorySearch.js')
            var.SearchHistoryProgramJson = json.loads(SearchHistorySearchString)
    except:
        var.SearchHistoryProgramJson = []

    try:
        if var.SearchHistoryChannelJson == [] and files.existFile('SearchHistoryChannel.js') == True:
            SearchHistorySearchString = files.openFile('SearchHistoryChannel.js')
            var.SearchHistoryChannelJson = json.loads(SearchHistorySearchString)
    except:
        var.SearchHistoryChannelJson = []

def search_history_add(searchTerm, searchChannel=False):
    #Check search term
    if func.string_isnullorempty(searchTerm) == True:
        return

    #Remove search term from Json
    search_history_remove(searchTerm, False, searchChannel)

    #Set Json target list variable
    if searchChannel == True:
        searchHistoryTargetFile = 'SearchHistoryChannel.js'
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    else:
        searchHistoryTargetFile = 'SearchHistorySearch.js'
        searchHistoryTargetJson = var.SearchHistoryProgramJson

    #Add search history to Json
    searchHistoryTargetJson.insert(0, searchTerm)

    #Trim search history length
    if len(searchHistoryTargetJson) > 40:
        searchHistoryTargetJson = searchHistoryTargetJson[:40]

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(searchHistoryTargetJson).encode('ascii')
    files.saveFile(searchHistoryTargetFile, JsonDumpBytes)

def search_history_remove(searchTerm, saveJson=True, searchChannel=False):
    #Set Json target list variable
    if searchChannel == True:
        searchHistoryTargetFile = 'SearchHistoryChannel.js'
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    else:
        searchHistoryTargetFile = 'SearchHistorySearch.js'
        searchHistoryTargetJson = var.SearchHistoryProgramJson

    #Remove search term from Json
    for search in searchHistoryTargetJson:
        try:
            if search == searchTerm:
                searchHistoryTargetJson.remove(search)
                break
        except:
            continue

    #Save the raw json data to storage
    if saveJson == True:
        JsonDumpBytes = json.dumps(searchHistoryTargetJson).encode('ascii')
        files.saveFile(searchHistoryTargetFile, JsonDumpBytes)

def search_dialog(headerText='Zoeken', searchChannel=False):
    #Load search history
    search_history_json_load()

    #Set Json target list variable
    if searchChannel == True:
        searchHistoryTargetFile = 'SearchHistoryChannel.js'
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    else:
        searchHistoryTargetFile = 'SearchHistorySearch.js'
        searchHistoryTargetJson = var.SearchHistoryProgramJson

    #Set search history
    dialogAnswers = hybrid.deep_copy_list(searchHistoryTargetJson)
    dialogAnswers.insert(0, '+ Nieuw zoek term gebruiken')

    dialogHeader = headerText
    dialogSummary = 'Selecteer een eerder gebruikte zoek term of klik op nieuw zoek term.'
    dialogFooter = ''

    #Select search string
    searchString = dialog.show_dialog(dialogHeader, dialogSummary, dialogFooter, dialogAnswers)

    #Check search string
    if searchString == '+ Nieuw zoek term gebruiken':
        keyboard = xbmc.Keyboard('default', 'heading')
        keyboard.setHeading(headerText)
        keyboard.setDefault('')
        keyboard.setHiddenInput(False)
        keyboard.doModal()
        if keyboard.isConfirmed() == True:
            #Get keyboard text
            keyboardText = keyboard.getText()

            #Add search history to Json
            search_history_add(keyboardText, searchChannel)

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
        search_history_add(searchString, searchChannel)

        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = searchString
        return searchResult
