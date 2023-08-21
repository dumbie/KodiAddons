from threading import Thread
import hybrid
import var

class ProxyRequestHandler(hybrid.proxyRequestHandler):
    def do_GET(self):
        try:
            if "/redir/" in self.path:
                fullUrl = self.path.replace('/redir/', '', 1)
                self.send_response(302)
                self.send_header('Location', fullUrl)
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Webbie Player proxy server is working.')
        except:
            pass

class ProxyRequestThreading(hybrid.proxyThreading, hybrid.proxyServer):
    pass

def thread_proxy_server():
    while var.thread_proxy_server != None and var.addonmonitor.abortRequested() == False: #Service thread no need to check addon running
        var.ProxyServer.handle_request()

def start_proxy_server():
    if var.ProxyServer == None:
        var.ProxyServer = ProxyRequestThreading(('127.0.0.1', 4444), ProxyRequestHandler)
        var.thread_proxy_server = Thread(target=thread_proxy_server)
        var.thread_proxy_server.start()

def stop_proxy_server():
    if var.ProxyServer != None:
        var.ProxyServer.shutdown()
        var.ProxyServer = None
        var.thread_proxy_server = None
