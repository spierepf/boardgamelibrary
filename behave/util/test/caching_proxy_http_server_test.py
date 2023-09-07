import requests

from util import CachingProxyHttpServer


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
