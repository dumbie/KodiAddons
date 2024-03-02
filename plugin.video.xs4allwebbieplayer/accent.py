import files
import getset
import path

#Get add-on accent color
def get_accent_color_hex():
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        return 'FFF5AF00'
    elif currentProvider == 'blauw':
        return 'FF2F41B7'
    elif currentProvider == 'groen':
        return 'FF009900'
    elif currentProvider == 'grijs':
        return 'FF888888'

#Get add-on accent color string
def get_accent_color_string():
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        return '[COLOR FFF5AF00]'
    elif currentProvider == 'blauw':
        return '[COLOR FF2F41B7]'
    elif currentProvider == 'groen':
        return '[COLOR FF009900]'
    elif currentProvider == 'grijs':
        return '[COLOR FF888888]'

#Change add-on accent images
def change_addon_accent():
    #Set image destination paths
    backgroundAddon = path.resources("resources/skins/default/media/common/background_addon.png")
    backgroundAccent = path.resources("resources/skins/default/media/common/background_accent.png")
    scrollbar400 = path.resources("resources/skins/default/media/common/scrollbar_accent_400.png")
    scrollbar800 = path.resources("resources/skins/default/media/common/scrollbar_accent_800.png")

    #Copy add-on accent images
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_yellow.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_yellow.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_yellow.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_yellow.png'), scrollbar800)
    elif currentProvider == 'blauw':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_blue.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_blue.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_blue.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_blue.png'), scrollbar800)
    elif currentProvider == 'groen':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_green.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_green.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_green.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_green.png'), scrollbar800)
    elif currentProvider == 'grijs':
        files.removeFile(backgroundAddon)
        files.copyFile(path.resources('resources/skins/default/media/common/background_addon_gray.png'), backgroundAddon)
        files.removeFile(backgroundAccent)
        files.copyFile(path.resources('resources/skins/default/media/common/background_accent_gray.png'), backgroundAccent)
        files.removeFile(scrollbar400)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_400_gray.png'), scrollbar400)
        files.removeFile(scrollbar800)
        files.copyFile(path.resources('resources/skins/default/media/common/scrollbar_accent_800_gray.png'), scrollbar800)

    #Copy custom background image
    if files.existFileUser(path.addonstorage("background.png")):
        files.removeFile(backgroundAddon)
        files.copyFile(path.addonstorage("background.png"), backgroundAddon)
