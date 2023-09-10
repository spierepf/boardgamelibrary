# https://www.django-rest-framework.org/#example

from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from library.models import Title


# Serializers define the API representation.
class TitleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'name', 'bgg_id']


# ViewSets define the view behavior.
class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]
