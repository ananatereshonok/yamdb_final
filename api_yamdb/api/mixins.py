from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import SearchFilter

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
