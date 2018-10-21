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
    from .permissions import IsOwner

    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser

    from django_filters.rest_framework.backends import DjangoFilterBackend

    # The filter backend classes to use for queryset filtering
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend)

    permission_classes = (IsOwner, )
    renderer_classes = (JSONRenderer, )
    parser_classes = (JSONParser, )


class GenericByUserAPIView(OwnerGenericAPIView):
    """
    Generic view where object is retrieved via logged in user and does not requires a primary key.
    Can be used in models having One-to-One relation with User model.
    """
    lookup_field = 'created_by'

    def get_object(self):
        self.kwargs[self.lookup_field] = self.request.user
        return super(GenericByUserAPIView, self).get_object()


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


class OwnerDestroyAPIView(mixins.DestroyModelMixin,
                          OwnerGenericAPIView):
    """
    Concrete view for deleting a CreateUpdateModel based model instance.
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OwnerUpdateAPIView(OwnerUpdateModelMixin,
                         OwnerGenericAPIView):
    """
    Concrete view for updating a CreateUpdateModel based model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OwnerListCreateAPIView(mixins.ListModelMixin,
                             OwnerCreateModelMixin,
                             OwnerGenericAPIView):
    """
    Concrete view for listing a queryset or creating a CreateUpdateModel based model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OwnerRetrieveUpdateAPIView(mixins.RetrieveModelMixin,
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


class OwnerRetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin,
                                  OwnerGenericAPIView):
    """
    Concrete view for retrieving or deleting a CreateUpdateModel based model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OwnerRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
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


class RetrieveByUserAPIView(mixins.RetrieveModelMixin,
                            GenericByUserAPIView):
    """
    Concrete view for retrieving a CreateUpdateModel based model instance where One-to-One relationship exists on
    created_by with User.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateByUserAPIView(OwnerUpdateModelMixin,
                          GenericByUserAPIView):
    """
    Concrete view for updating a CreateUpdateModel based model instance where One-to-One relationship exists on
    created_by with User.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DestroyByUserAPIView(mixins.DestroyModelMixin,
                           GenericByUserAPIView):
    """
    Concrete view for deleting a CreateUpdateModel based model instance where One-to-One relationship exists on
    created_by with User.
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateByUserAPIView(mixins.RetrieveModelMixin,
                                  OwnerUpdateModelMixin,
                                  GenericByUserAPIView):
    """
    Concrete view for retrieving, updating a CreateUpdateModel based model instance where One-to-One relationship
    exists on created_by with User.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyByUserAPIView(mixins.RetrieveModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericByUserAPIView):
    """
    Concrete view for retrieving or deleting a CreateUpdateModel based model instance where One-to-One relationship
    exists on created_by with User.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyByUserAPIView(mixins.RetrieveModelMixin,
                                         OwnerUpdateModelMixin,
                                         mixins.DestroyModelMixin,
                                         GenericByUserAPIView):
    """
    Concrete view for retrieving, updating or deleting a CreateUpdateModel based model instance where One-to-One
    relationship exists on created_by with User.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CreateRetrieveUpdateDestroyByUserAPIView(OwnerCreateModelMixin,
                                               mixins.RetrieveModelMixin,
                                               OwnerUpdateModelMixin,
                                               mixins.DestroyModelMixin,
                                               GenericByUserAPIView):
    """
    Concrete view for adding, retrieving, updating or deleting a CreateUpdateModel based model instance where
    One-to-One relationship exists on created_by with User.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
