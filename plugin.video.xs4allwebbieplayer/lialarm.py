import alarm
import func
import lifunc
import xbmcgui
import path
import var

def list_load_combined(listContainer=None, forceLoad=False):
    try:
        #Load set program alarms
        alarm.alarm_json_load(forceLoad)

        #Add items to sort list
        listContainerSort = []
        list_load_append(listContainerSort)

        #Sort list items
        listContainerSort.sort(key=lambda x: x.getProperty('ProgramTimeStart'))

        #Add items to container
        lifunc.auto_add_items(listContainerSort, listContainer)
        lifunc.auto_end_items()
        return True
    except:
        return False

def list_load_append(listContainer):
    for alarm in var.AlarmDataJson:
        try:
            ExternalId = alarm['externalid']
            ProgramName = alarm['programname']
            ProgramTimeStart = alarm['starttime']

            ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStart, '%Y-%m-%d %H:%M:%S')
            ProgramDescription = 'Om ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' op ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            #Set item icons
            iconDefault = path.icon_television(ExternalId)

            #Set item details
            listItem = xbmcgui.ListItem()
            listItem.setProperty('ProgramTimeStart', ProgramTimeStart)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setArt({'thumb': iconDefault, 'icon': iconDefault, 'poster': iconDefault})
            listContainer.append(listItem)
        except:
            continue
