from http.server import HTTPServer, BaseHTTPRequestHandler

class MinimalHTTPRequestHandler(BaseHTTPRequestHandler):
    """implements a minimal HTTP server that serves an empty page on GET and POST"""
    def _set_headers(self):
        """Set the response headers and status"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        self._set_headers()

    def do_HEAD(self):
        """Handle HEAD requests"""
        self._set_headers()
        
    def do_POST(self):
        """Handle POST requests"""
        self._set_headers()
