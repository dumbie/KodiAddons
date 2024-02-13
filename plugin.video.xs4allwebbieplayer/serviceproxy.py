import hybrid
import var
import path
import xbmcgui

class ProxyRequestHandler(hybrid.proxyRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        try:
            if "/redir/" in self.path:
                fullUrl = self.path.replace('/redir/', '', 1)
                self.send_response(302)
                self.send_header('Location', fullUrl)
                self.end_headers()
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
            var.thread_proxy_server.Start(thread_proxy_server)
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, "Proxy server starten mislukt", notificationIcon, 2500, False)

def stop_proxy_server():
    try:
        if var.ProxyServer != None:
            var.ProxyServer.shutdown()
            var.ProxyServer.server_close()
            var.ProxyServer = None
            var.thread_proxy_server.Stop()
    except:
        notificationIcon = path.resources('resources/skins/default/media/common/error.png')
        xbmcgui.Dialog().notification(var.addonname, "Proxy server stoppen mislukt", notificationIcon, 2500, False)
