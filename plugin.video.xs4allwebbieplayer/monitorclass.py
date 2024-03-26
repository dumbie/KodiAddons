import xbmc
import xbmcaddon
import accent
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
