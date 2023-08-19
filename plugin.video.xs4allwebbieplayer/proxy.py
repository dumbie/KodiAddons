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

def start_proxy_server():
    if var.ProxyServer == None:
        var.ProxyServer = hybrid.proxyServer(('', 4444), ProxyRequestHandler)
        var.ProxyServer.serve_forever()

def stop_proxy_server():
    if var.ProxyServer != None:
        var.ProxyServer.shutdown()
        var.ProxyServer = None
