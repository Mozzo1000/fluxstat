from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http import HTTPStatus
import json
import signal
import sys
from datetime import datetime
import time
import psutil
from metrics import CPU, Memory, Disk

class FluxRequestHandler(BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_HEAD(self):
        self.set_headers()

    def do_GET(self):
        response = {}
        if self.path == "/metrics":
            response = {
                "system": {
                    "uptime: ": round(time.time() - psutil.boot_time()),
                    "cpu": CPU().toJSON(),
                    "memory": Memory().toJSON(),
                    "disk": Disk().toJSON()
                },
                "updated_at": datetime.now().isoformat()
            }
        else:
            # TODO: Change message to send json instead of the default html
            self.send_error(HTTPStatus.NOT_FOUND.value)

        self.send_response(HTTPStatus.OK.value)
        self.set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run_server():
    server_address = ('', 8001)
    httpd = ThreadingHTTPServer(server_address, FluxRequestHandler)

    def signal_handler(sig, frame):
        print('Closing server..')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('fluxstat serving at %s:%d' % server_address)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
