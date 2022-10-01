from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http import HTTPStatus
import json
import signal
import sys
from datetime import datetime
import time
import argparse
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
            self.error_content_type = "application/json"
            self.error_message_format = '{"status": %(code)d, "message": "%(message)s"}'
            self.send_error(HTTPStatus.NOT_FOUND.value, "Not found")

        self.send_response(HTTPStatus.OK.value)
        self.set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def main():

    parser = argparse.ArgumentParser("Fluxstate Agent")
    parser.add_argument("-a", "--address", type=str, default="localhost", help="Address of http server")
    parser.add_argument("-p", "--port", type=int, default=8001, help="Port of http server")

    server_address = (parser.parse_args().address, parser.parse_args().port)
    httpd = ThreadingHTTPServer(server_address, FluxRequestHandler)

    def signal_handler(sig, frame):
        print('Closing server..')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('fluxstat serving at %s:%d' % server_address)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
