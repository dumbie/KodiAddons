import xbmc
import xbmcaddon
import accent
import alarmfunc
import cache

class Class_MonitorCustom(xbmc.Monitor):
    #Settings cache
    AddonAccentCache = xbmcaddon.Addon().getSetting('AddonAccent')
    TelevisionChannelNoEroticCache = xbmcaddon.Addon().getSetting('TelevisionChannelNoErotic')

    #Check changed settings
    def onSettingsChanged(self):
        AddonAccentCurrent = xbmcaddon.Addon().getSetting('AddonAccent')
        if self.AddonAccentCache != AddonAccentCurrent:
            self.AddonAccentCache = AddonAccentCurrent
            accent.change_addon_accent()

        TelevisionChannelNoEroticCurrent = xbmcaddon.Addon().getSetting('TelevisionChannelNoErotic')
        if self.TelevisionChannelNoEroticCache != TelevisionChannelNoEroticCurrent:
            self.TelevisionChannelNoEroticCache = TelevisionChannelNoEroticCurrent
            cache.cache_remove_all(False, True)

    #Check incoming notifications
    def onNotification(self, sender, method, data):
        if sender == 'WebbiePlayer' and method == 'Other.alarm_reload':
            alarmfunc.alarm_json_load(True)
            alarmfunc.alarm_update_interface()
        elif sender == 'WebbiePlayer' and method == 'Other.cache_reset':
            cache.cache_reset_variables(data)
