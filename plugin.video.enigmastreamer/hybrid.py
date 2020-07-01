import sys

pythonversion = sys.version_info[0]
if pythonversion < 3:
    import urllib2
    from HTMLParser import HTMLParser
    inputstreamname = 'inputstreamaddon'
else:
    import urllib.request, urllib.parse
    from html.parser import HTMLParser
    inputstreamname = 'inputstream'

#String decode utf8
def string_decode_utf8(string):
    if pythonversion < 3:
        return string.decode('UTF-8')
    else:
        return string

#Urllib request
def urllib_request(*args, **kwargs):
    if pythonversion < 3:
        return urllib2.Request(*args, **kwargs)
    else:
        return urllib.request.Request(*args, **kwargs)

#Urllib urlopen
def urllib_urlopen(*args, **kwargs):
    if pythonversion < 3:
        return urllib2.urlopen(*args, **kwargs)
    else:
        return urllib.request.urlopen(*args, **kwargs)

#Urllib getheader
def urllib_getheader(urlOpen, headerName):
    if pythonversion < 3:
        return urlOpen.info().getheader(headerName)
    else:
        return urlOpen.getheader(headerName)

#Urllib quote
def urllib_quote(string):
    if pythonversion < 3:
        return urllib2.quote(string)
    else:
        return urllib.parse.quote(string)

#Urllib unquote
def urllib_unquote(string):
    if pythonversion < 3:
        return urllib2.unquote(string)
    else:
        return urllib.parse.unquote(string)

#Htmlparser unescape
def htmlparser_unescape(string):
    return HTMLParser().unescape(string)
