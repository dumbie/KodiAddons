from threading import Thread
from xml.dom import minidom
import hybrid
import var
import path
import xbmc
import xbmcgui

class ProxyRequestHandler(hybrid.proxyRequestHandler):
    def proxy_redirect(self, fullUrl):
        try:
            self.send_response(302)
            self.send_header('Location', fullUrl)
            self.end_headers()
        except:
            pass

    def proxy_redirect_cenc(self, fullUrl):
        try:
            #Set the download headers
            DownloadHeaders = {
                "User-Agent": var.addon.getSetting('CustomUserAgent')
            }

            #Download CBCS mpd
            DownloadRequest = hybrid.urllib_request(fullUrl, headers=DownloadHeaders)
            DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)

            #Forward CENC mpd
            fullUrl = fullUrl.replace('v.isml/', '.isml/')
            self.send_response(302)
            self.send_header('Location', fullUrl)
            self.end_headers()
        except:
            pass

    def proxy_mpd_edit(self, fullUrl):
        try:
            #Set the download headers
            DownloadHeaders = {
                "User-Agent": var.addon.getSetting('CustomUserAgent')
            }

            #Download CBCS mpd
            DownloadRequest = hybrid.urllib_request(fullUrl, headers=DownloadHeaders)
            DownloadDataHttp = hybrid.urllib_urlopen(DownloadRequest)
            xmlParseCBCS = minidom.parse(DownloadDataHttp)

            #Edit CBCS mpd
            for xmlAdaptSet in xmlParseCBCS.getElementsByTagName('AdaptationSet'):
                adaptSetContentType = xmlAdaptSet.getAttribute('contentType')
                if adaptSetContentType == 'audio':
                    for xmlElement in xmlAdaptSet.getElementsByTagName('AudioChannelConfiguration'):
                        #if xmlElement.getAttribute('schemeIdUri') == 'tag:dolby.com,2014:dash:audio_channel_configuration:2011':
                        #Get configuration
                        parent0 = xmlElement.parentNode

                        #Get adaption set
                        parent1 = parent0.parentNode
                        parent1.removeChild(parent0)

            #Encode CBCS mpd
            xmlDecoded = xmlParseCBCS.toxml()
            xmlEncoded = xmlDecoded.encode()
            xbmc.log('Webbie Player Proxy MPD:\n' + xmlDecoded, xbmc.LOGDEBUG)

            self.send_response(200)
            self.send_header('Content-Type', 'application/dash+xml')
            self.send_header("Content-Length", len(xmlEncoded))
            self.end_headers()
            self.wfile.write(xmlEncoded)
        except:
            pass

    def do_GET(self):
        try:
            if "/redir/" in self.path:
                fullUrl = self.path.replace('/redir/', '', 1)
                if '.mpd' in fullUrl.lower():
                    self.proxy_mpd_edit(fullUrl)
                else:
                    self.proxy_redirect(fullUrl)
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Webbie Player proxy server is working.')
        except:
            pass

class ProxyRequestThreading(hybrid.proxyThreading, hybrid.proxyServer):
    pass

def thread_proxy_server():
    try:
        if var.ProxyServer != None:
            var.ProxyServer.serve_forever()
    except:
        pass

def start_proxy_server():
    try:
        if var.ProxyServer == None:
            var.ProxyServer = ProxyRequestThreading(('127.0.0.1', 4444), ProxyRequestHandler)
            if var.thread_proxy_server == None:
                var.thread_proxy_server = Thread(target=thread_proxy_server)
                var.thread_proxy_server.start()
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, "Proxy server starten mislukt", notificationIcon, 2500, False)

def stop_proxy_server():
    try:
        if var.ProxyServer != None:
            var.ProxyServer.shutdown()
            var.ProxyServer.server_close()
            var.ProxyServer = None
            var.thread_proxy_server = None
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, "Proxy server stoppen mislukt", notificationIcon, 2500, False)
