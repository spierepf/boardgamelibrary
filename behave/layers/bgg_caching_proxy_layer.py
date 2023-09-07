import pathlib

from util import CachingProxyHttpServer

from .behave_layer import BehaveLayer


class BggCachingProxyLayer(BehaveLayer):
    def __init__(self):
        self.cached_responses_file = (pathlib.Path(__file__).parent.parent / 'resources' / 'bgg_cached_responses.json')

    def before_all(self, context):
        if self.cached_responses_file.exists():
            with open(self.cached_responses_file.resolve(), 'r') as f:
                cached_responses = f.read()
        else:
            cached_responses = '{}'
        context.bgg_proxy = CachingProxyHttpServer('https://boardgamegeek.com', cached_responses)

    def after_all(self, context):
        with open(self.cached_responses_file.resolve(), 'w') as f:
            f.write(context.bgg_proxy.export_cached_responses())

