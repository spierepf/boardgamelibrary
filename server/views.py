import os

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['groups'] = list([it.name for it in user.groups.all()])

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@api_view(['GET'])
def client_configuration(request):
    bgg_base_url = os.environ.get('BGG_BASE_URL', 'https://boardgamegeek.com')
    return JsonResponse({'bgg_base_url': bgg_base_url})
