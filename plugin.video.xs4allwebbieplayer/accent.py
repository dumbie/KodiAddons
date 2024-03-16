import getset

#Get add-on accent color string
def get_accent_color_string():
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        return '[COLOR FFB38300]'
    elif currentProvider == 'blauw':
        return '[COLOR FF2D43B3]'
    elif currentProvider == 'groen':
        return '[COLOR FF008500]'
    elif currentProvider == 'grijs':
        return '[COLOR FF888888]'
    elif currentProvider == 'rood':
        return '[COLOR FFB32430]'

#Change add-on accent variables
def change_addon_accent():
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        getset.global_set('ColorAccent', 'FFB38300')
        getset.global_set('ColorFocused', 'F5664B00')
    elif currentProvider == 'blauw':
        getset.global_set('ColorAccent', 'FF2D43B3')
        getset.global_set('ColorFocused', 'F51A2666')
    elif currentProvider == 'groen':
        getset.global_set('ColorAccent', 'FF008500')
        getset.global_set('ColorFocused', 'F5004D00')
    elif currentProvider == 'grijs':
        getset.global_set('ColorAccent', 'FF444444')
        getset.global_set('ColorFocused', 'F5333333')
    elif currentProvider == 'rood':
        getset.global_set('ColorAccent', 'FFB32430')
        getset.global_set('ColorFocused', 'F566141B')
    getset.global_set('ColorNoFocus', 'FF181818')
