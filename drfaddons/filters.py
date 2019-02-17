"""
Custom filters that are used in generics API Views

Author: Himanshu Shankar (https://himanshus.com)
"""

from rest_framework.filters import BaseFilterBackend


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    Filters data as per ownership
    Source: http://www.django-rest-framework.org/api-guide/filtering/
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(created_by=request.user)


class IsOwnerOrSuperuser(IsOwnerFilterBackend):
    """
    Filters data as per ownership, is user is not a superuser

    Author: Himanshu Shankar (https://himanshus.com)
    """
    def filter_queryset(self, request, queryset, view):
        if not request.user.is_superuser:
            return super(IsOwnerOrSuperuser, self).filter_queryset(
                request=request, queryset=request, view=view
            )
        else:
            return queryset
