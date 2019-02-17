"""
Custom abstract models that provides various functionality and can be
inherited for further use.

Author: Himanshu Shankar
"""

from django.db import models


class CreateUpdateModel(models.Model):
    """
    An abstract model that provides 3 field in every inherited model.
    create_date: Sets up the create date of any object
    update_date: Sets up the last update date of any object
    created_by: Sets up the user ID of creator with the object

    Author: Himanshu Shankar (https://himanshus.com)
    """
    from django.contrib.auth import get_user_model
    from django.utils.text import gettext_lazy as _

    create_date = models.DateTimeField(_('Create Date/Time'),
                                       auto_now_add=True)
    update_date = models.DateTimeField(_('Date/Time Modified'),
                                       auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.PROTECT)

    def is_owner(self, user):
        """
        Checks if user is the owner of object

        Parameters
        ----------
        user: get_user_model() instance

        Returns
        -------
        bool

        Author
        ------
        Himanshu Shankar (https://himanshus.com)
        """
        if user.is_authenticated:
            return self.created_by.id == user.id
        return False

    def has_permission(self, user):
        """
        Checks if the provided user has permission on provided object

        Parameters
        ----------
        user: get_user_model() instance

        Returns
        -------
        bool

        Author
        ------
        Himanshu Shankar (https://himanshus.com)
        """
        return self.is_owner(user)

    class Meta:
        abstract = True
