from http.server import HTTPServer, BaseHTTPRequestHandler

class MinimalHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()
