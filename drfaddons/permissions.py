from rest_framework.permissions import IsAuthenticated


class IsOwner(IsAuthenticated):
    """
    Implements `has_object_permission` along in IsAuthenticated
    """
    def has_object_permission(self, request, view, obj):
        """
        Checks if the provided object has a created_by field and if request.user is the owner of object.
        Parameters
        ----------
        request
        view
        obj

        Returns
        -------
        bool: True, either if request.user is the creator of object or if object doesn't have created_by object
              False, if object has created_by field but it is not same as request.user
        """
        if hasattr(obj, 'created_by'):
            if obj.created_by == request.user:
                return True
            else:
                return False
        else:
            return True
