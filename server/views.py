import os

from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def client_configuration(request):
    bgg_base_url = os.environ.get('BGG_BASE_URL', 'https://boardgamegeek.com')
    return JsonResponse({'bgg_base_url': bgg_base_url})
