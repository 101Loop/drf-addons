"""
Custom Mixins for future use cases.

Author: Himanshu Shankar (https://himanshus.com)
"""

from __future__ import unicode_literals

from rest_framework.mixins import CreateModelMixin


class OwnerCreateModelMixin(CreateModelMixin):
    """
    Create a CreateUpdateModel based model instance.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
