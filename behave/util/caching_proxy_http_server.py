import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

import requests


class CachingProxyHttpServer(HTTPServer):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            request_path = self.path
            if request_path not in self.server.cached_responses.keys():
                response = requests.get(f"{self.server.remote_target}{request_path}")
                cached_response = {
                    "content_type": response.headers['Content-type'],
                    "status_code": response.status_code,
                    "text": response.text
                }

                self.server.cached_responses[request_path] = cached_response
                self.server.cache_miss_count += 1

            cached_response = self.server.cached_responses[request_path]
            self.send_response(cached_response["status_code"])
            self.send_header("Content-type", cached_response["content_type"])
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(cached_response["text"].encode("utf-8"))

    def __init__(self, remote_target, cached_responses_json='{}'):
        super().__init__(('localhost', 0), self.Handler)
        self.remote_target = remote_target
        self.thread = Thread(target=lambda: self.serve_forever())
        self.thread.daemon = True
        self.cached_responses = json.loads(cached_responses_json)
        self.cache_miss_count = 0
        self.thread.start()

    def root(self):
        return f"http://{self.server_name}:{self.server_port}"

    def export_cached_responses(self):
        return json.dumps(self.cached_responses)
