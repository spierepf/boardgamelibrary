# https://www.django-rest-framework.org/#example
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.relations import PrimaryKeyRelatedField

# https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html
from django_filters import rest_framework as filters

from library.models import Title, Copy


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TitleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'name', 'bgg_id']


class CopySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Copy
        fields = ['id', 'uuid', 'title', 'owner']


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


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedAsAdminOrCommitteeOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedAsAdminOrCommitteeOrReadOnly]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name', 'bgg_id')


class CopyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedAsAdminOrCommitteeOrReadOnly]
    queryset = Copy.objects.all()
    serializer_class = CopySerializer
    filter_backends = (filters.DjangoFilterBackend,)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'copies', CopyViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]
