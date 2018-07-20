from __future__ import unicode_literals

from rest_framework.mixins import CreateModelMixin, UpdateModelMixin


class OwnerCreateModelMixin(CreateModelMixin):
    """
    Create a CreateUpdateModel based model instance.
    """

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class OwnerUpdateModelMixin(UpdateModelMixin):
    """
    Updates a CreateUpdateModel based model instance.
    """

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)
