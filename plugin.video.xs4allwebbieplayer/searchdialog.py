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
            SearchHistoryJsonString = files.openFile('SearchHistorySearch.js')
            var.SearchHistoryProgramJson = json.loads(SearchHistoryJsonString)
    except:
        var.SearchHistoryProgramJson = []

    try:
        if var.SearchHistoryChannelJson == [] and files.existFile('SearchHistoryChannel.js') == True:
            SearchHistoryJsonString = files.openFile('SearchHistoryChannel.js')
            var.SearchHistoryChannelJson = json.loads(SearchHistoryJsonString)
    except:
        var.SearchHistoryChannelJson = []

    try:
        if var.SearchHistoryRadioJson == [] and files.existFile('SearchHistoryRadio.js') == True:
            SearchHistoryJsonString = files.openFile('SearchHistoryRadio.js')
            var.SearchHistoryRadioJson = json.loads(SearchHistoryJsonString)
    except:
        var.SearchHistoryRadioJson = []

def search_history_add(searchTerm, searchJsonFile):
    #Check search term
    if func.string_isnullorempty(searchTerm) == True:
        return

    #Remove search term from Json
    search_history_remove(searchTerm, searchJsonFile, False)

    #Set Json target list variable
    if searchJsonFile == 'SearchHistoryChannel.js':
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFile == 'SearchHistoryRadio.js':
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFile == 'SearchHistorySearch.js':
        searchHistoryTargetJson = var.SearchHistoryProgramJson

    #Add search history to Json
    searchHistoryTargetJson.insert(0, searchTerm)

    #Trim search history length
    if len(searchHistoryTargetJson) > 40:
        searchHistoryTargetJson = searchHistoryTargetJson[:40]

    #Save the raw json data to storage
    JsonDumpBytes = json.dumps(searchHistoryTargetJson).encode('ascii')
    files.saveFile(searchJsonFile, JsonDumpBytes)

def search_history_remove(searchTerm, searchJsonFile, saveJson=True):
    #Set Json target list variable
    if searchJsonFile == 'SearchHistoryChannel.js':
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFile == 'SearchHistoryRadio.js':
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFile == 'SearchHistorySearch.js':
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
        files.saveFile(searchJsonFile, JsonDumpBytes)

def search_dialog(searchJsonFile, headerText='Zoeken'):
    #Load search history
    search_history_json_load()

    #Set Json target list variable
    if searchJsonFile == 'SearchHistoryChannel.js':
        searchHistoryTargetJson = var.SearchHistoryChannelJson
    elif searchJsonFile == 'SearchHistoryRadio.js':
        searchHistoryTargetJson = var.SearchHistoryRadioJson
    elif searchJsonFile == 'SearchHistorySearch.js':
        searchHistoryTargetJson = var.SearchHistoryProgramJson

    #Set search history
    dialogAnswers = hybrid.deep_copy_list(searchHistoryTargetJson)
    dialogAnswers.insert(0, '- Leeg zoek term gebruiken')
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
            search_history_add(keyboardText, searchJsonFile)

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
    elif searchString == '- Leeg zoek term gebruiken':
        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
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
        search_history_add(searchString, searchJsonFile)

        #Return search result
        searchResult = classes.Class_SearchResult()
        searchResult.cancelled = False
        searchResult.string = searchString
        return searchResult
