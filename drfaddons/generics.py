"""
Generic views that provide commonly needed behaviour for CreateUpdateModel.
"""
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from .mixins import OwnerCreateModelMixin, OwnerUpdateModelMixin


class OwnerGenericAPIView(GenericAPIView):
    """
    Base class for all other generic views based on CreateUpdateModel.
    Only allows Authenticated User
    Uses JSONParser & JSONRenderer
    """
    from .filters import IsOwnerFilterBackend

    from rest_framework.permissions import IsAuthenticated
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser

    from django_filters.rest_framework.backends import DjangoFilterBackend

    # The filter backend classes to use for queryset filtering
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    parser_classes = (JSONParser, )


# Concrete view classes that provide method handlers
# by composing the mixin classes with the base view.
# Only for CreateUpdateModel this package

class OwnerCreateAPIView(OwnerCreateModelMixin,
                         OwnerGenericAPIView):
    """
    Concrete view for creating a CreateUpdateModel based model instance.
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OwnerListAPIView(mixins.ListModelMixin,
                       OwnerGenericAPIView):
    """
    Concrete view for listing a CreateUpdateModel based queryset.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OwnerRetrieveAPIView(mixins.RetrieveModelMixin,
                           OwnerGenericAPIView):
    """
    Concrete view for retrieving a CreateUpdateModel based model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(mixins.DestroyModelMixin,
                     OwnerGenericAPIView):
    """
    Concrete view for deleting a CreateUpdateModel based model instance.
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(OwnerUpdateModelMixin,
                    OwnerGenericAPIView):
    """
    Concrete view for updating a CreateUpdateModel based model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin,
                        OwnerCreateModelMixin,
                        OwnerGenericAPIView):
    """
    Concrete view for listing a queryset or creating a CreateUpdateModel based model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            OwnerUpdateModelMixin,
                            OwnerGenericAPIView):
    """
    Concrete view for retrieving, updating a CreateUpdateModel based model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             OwnerGenericAPIView):
    """
    Concrete view for retrieving or deleting a CreateUpdateModel based model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   OwnerUpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   OwnerGenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a CreateUpdateModel based model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
