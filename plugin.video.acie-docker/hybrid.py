import sys
import unicodedata

pythonversion = sys.version_info[0]
if pythonversion < 3:
    import xbmc
    import urllib2
    from urllib import urlencode
    from urlparse import parse_qsl
    from HTMLParser import HTMLParser
    htmlx = HTMLParser()
    inputstreamname = 'inputstreamaddon'
    import SimpleHTTPServer
    import SocketServer
    proxyServer = SocketServer.TCPServer
    proxyThreading = SocketServer.ThreadingMixIn
    proxyRequestHandler = SimpleHTTPServer.SimpleHTTPRequestHandler
    from StringIO import StringIO
else:
    import xbmcvfs
    import urllib.request, urllib.parse
    from urllib.parse import urlencode
    from urllib.parse import parse_qsl
    import html
    htmlx = html
    inputstreamname = 'inputstream'
    import http.server as SimpleHTTPServer
    import socketserver
    proxyServer = socketserver.TCPServer
    proxyThreading = socketserver.ThreadingMixIn
    proxyRequestHandler = SimpleHTTPServer.BaseHTTPRequestHandler
    from io import BytesIO

#Xbmc translate path
def xbmc_translate_path(path):
    if pythonversion < 3:
        return xbmc.translatePath(path)
    else:
        return xbmcvfs.translatePath(path)

#Deep copy list to new list
def deep_copy_list(copyList):
    return copyList[:]

#Remove character accents from string
def string_remove_accents(string):
    if pythonversion < 3:
        if type(string) != unicode:
            string = string_to_unicode(string)
        uniString = ''.join(c for c in unicodedata.normalize('NFKD', string) if unicodedata.category(c) != 'Mn')
        uniString = string_encode_ascii(uniString)
        return string_decode_utf8(uniString)
    else:
        return ''.join(c for c in unicodedata.normalize('NFKD', string) if unicodedata.category(c) != 'Mn')

#Unicode to string
def unicode_to_string(string):
    if pythonversion < 3:
        if type(string) == unicode:
            uniString = ''.join(c for c in unicodedata.normalize('NFKD', string) if unicodedata.category(c) != 'Mn')
            uniString = string_encode_ascii(uniString)
            return string_decode_utf8(uniString)
    return string

#String to unicode
def string_to_unicode(string):
    if pythonversion < 3:
        if type(string) != unicode:
            return unicode(string, 'UTF-8')
    return string

#String encode utf8
def string_encode_utf8(string):
    if pythonversion < 3:
        return string.encode('UTF-8')
    else:
        if type(string) == bytes:
            return string.encode('UTF-8')
        else:
            return string

#String decode utf8
def string_decode_utf8(string):
    if pythonversion < 3:
        return string.decode('UTF-8')
    else:
        if type(string) == bytes:
            return string.decode('UTF-8')
        else:
            return string

#String encode ascii
def string_encode_ascii(string):
    if pythonversion < 3:
        return string.encode('ASCII', 'ignore')
    else:
        if type(string) == bytes:
            return string.encode('ASCII', 'ignore')
        else:
            return string

#String decode ascii
def string_decode_ascii(string):
    if pythonversion < 3:
        return string.decode('ASCII', 'ignore')
    else:
        if type(string) == bytes:
            return string.decode('ASCII', 'ignore')
        else:
            return string

#String io from bytes
def stringio_from_bytes(stringBytes):
    if pythonversion < 3:
        return StringIO(stringBytes)
    else:
        return BytesIO(stringBytes)

#Urllib request
def urllib_request(*args, **kwargs):
    if pythonversion < 3:
        return urllib2.Request(*args, **kwargs)
    else:
        return urllib.request.Request(*args, **kwargs)

#Urllib urlopen
def urllib_urlopen(*args, **kwargs):
    if pythonversion < 3:
        return urllib2.urlopen(timeout=10, *args, **kwargs)
    else:
        return urllib.request.urlopen(timeout=10, *args, **kwargs)

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
    return htmlx.unescape(string)
