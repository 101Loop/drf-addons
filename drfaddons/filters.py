"""
Custom filters that are used in generics API Views

Author: Himanshu Shankar (https://himanshus.com)
"""

from rest_framework.filters import BaseFilterBackend


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    This filter only allows users to see their own object
    Source: http://www.django-rest-framework.org/api-guide/filtering/
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(created_by=request.user)
