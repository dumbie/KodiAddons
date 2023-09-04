from datetime import datetime, timedelta
import func
import xbmcgui
import path
import var

def list_load(listContainer):
    for alarm in var.AlarmDataJson:
        try:
            ExternalId = alarm['externalid']
            #ChannelName = alarm['channelname']
            ProgramName = alarm['programname']
            ProgramTimeStart = alarm['starttime']

            ProgramTimeStartDateTime = func.datetime_from_string(ProgramTimeStart, '%Y-%m-%d %H:%M:%S')
            ProgramDescription = 'Om ' + ProgramTimeStartDateTime.strftime('%H:%M') + ' op ' + ProgramTimeStartDateTime.strftime('%a, %d %B %Y')

            listItem = xbmcgui.ListItem()
            listItem.setProperty('ProgramTimeStart', ProgramTimeStart)
            listItem.setProperty('ProgramName', ProgramName)
            listItem.setProperty('ProgramDescription', ProgramDescription)
            listItem.setArt({'thumb': path.icon_television(ExternalId), 'icon': path.icon_television(ExternalId)})
            listContainer.append(listItem)
        except:
            continue