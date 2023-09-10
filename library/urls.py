# https://www.django-rest-framework.org/#example

from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from library.models import Title


# Serializers define the API representation.
class TitleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'name', 'bgg_id']


# ViewSets define the view behavior.
class IsAuthenticatedAsAdminOrCommitteeOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin or committee user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            (request.user.groups.filter(name='ADMIN').exists() or request.user.groups.filter(name='COMMITTEE').exists())
        )


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedAsAdminOrCommitteeOrReadOnly]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]
