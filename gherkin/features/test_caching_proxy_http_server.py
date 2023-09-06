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


def test_cphs_caches_identical_requests():
    server = CachingProxyHttpServer('https://example.com')
    for _ in range(3):
        response = requests.get(f"{server.root()}/")
        assert response.status_code == 200
        assert response.text.startswith("<!doctype html>")

    assert server.cache_miss_count == 1


def test_cphs_export_import_cached_responses():
    exporting_server = CachingProxyHttpServer('https://example.com')
    requests.get(f"{exporting_server.root()}/")

    cached_responses_json = exporting_server.export_cached_responses()

    importing_server = CachingProxyHttpServer('https://example.com', cached_responses_json)
    requests.get(f"{importing_server.root()}/")

    assert importing_server.cache_miss_count == 0


def test_cphs_with_boardgamegeek():
    server = CachingProxyHttpServer('https://boardgamegeek.com')
    for _ in range(3):
        response = requests.get(
            f"{server.root()}/xmlapi2/search?type=boardgame,boardgameaccessory,boardgameexpansion&query=crossbows")
        assert response.status_code == 200
        assert response.text.startswith('<?xml version="1.0" encoding="utf-8"?>')
        assert len(response.text) > 256

    assert server.cache_miss_count == 1
