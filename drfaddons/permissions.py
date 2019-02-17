"""
Custom permissions that provides check of ownership.

Author: Himanshu Shankar (https://himanshus.com)
"""

from rest_framework.permissions import IsAuthenticated


class IsOwner(IsAuthenticated):
    """
    Implements `has_object_permission` to check for ownership
    IsAuthenticated

    Author: Himanshu Shankar (https://himanshus.com)
    """
    def has_object_permission(self, request, view, obj):
        """
        Checks if `request.user` is the owner of `obj`

        Parameters
        ----------
        request
        view
        obj

        Returns
        -------
        bool: True, either if request.user is the creator of object or
        if object doesn't have created_by object
              False, if object has created_by field but it is not same
              as request.user
        """
        return obj.is_owner(request.user)


class IsAuthenticatedWithPermission(IsAuthenticated):
    """
    Implements `has_object_permission` to check for object level
    permission

    Author: Himanshu Shankar (https://himanshus.com)
    """
    def has_object_permission(self, request, view, obj):
        """
        Checks if `request.user` has permission via
        `obj.has_permission()`

        Parameters
        ----------
        request
        view
        obj

        Returns
        -------

        """
        return obj.has_permission(request.user)


class IAWPOrSuperuser(IsAuthenticatedWithPermission):
    def has_object_permission(self, request, view, obj):
        """
        Checks if user is superuser or it has permission over object

        Parameters
        ----------
        request
        view
        obj

        Returns
        -------

        """
        return (
            request.user.is_superuser or
            super(IAWPOrSuperuser, self).has_object_permission(
                request=request, view=view, obj=obj
            )
        )
