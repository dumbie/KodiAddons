import getset

#Get add-on accent color string
def get_accent_color_string():
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        return '[COLOR FFA87B00]'
    elif currentProvider == 'blauw':
        return '[COLOR FF203D80]'
    elif currentProvider == 'groen':
        return '[COLOR FF007300]'
    elif currentProvider == 'rood':
        return '[COLOR FF981C26]'
    elif currentProvider == 'oranje':
        return '[COLOR FFCC5200]'
    elif currentProvider == 'grijs':
        return '[COLOR FF888888]'

#Change add-on accent variables
def change_addon_accent():
    currentProvider = getset.setting_get('AddonAccent').lower()
    if currentProvider == 'geel':
        getset.global_set('ColorAccent', 'FFA87B00')
        getset.global_set('ColorFocused', 'F5705200')
    elif currentProvider == 'blauw':
        getset.global_set('ColorAccent', 'FF203D80')
        getset.global_set('ColorFocused', 'F513244d')
    elif currentProvider == 'groen':
        getset.global_set('ColorAccent', 'FF007300')
        getset.global_set('ColorFocused', 'F5004700')
    elif currentProvider == 'rood':
        getset.global_set('ColorAccent', 'FF981C26')
        getset.global_set('ColorFocused', 'F5611118')
    elif currentProvider == 'grijs':
        getset.global_set('ColorAccent', 'FF454545')
        getset.global_set('ColorFocused', 'F5353535')
    elif currentProvider == 'oranje':
        getset.global_set('ColorAccent', 'FFCC5200')
        getset.global_set('ColorFocused', 'F5662900')
    getset.global_set('ColorNoFocus', 'FF181818')
