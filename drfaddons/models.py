from django.db import models


class CreateUpdateModel(models.Model):
    """
    An abstract model that provides 3 field in every inherited model.
    create_date: Sets up the create date of any object
    update_date: Sets up the last update date of any object
    created_by: Sets up the user ID of creator with the object

    Source: Himanshu Shankar (https://github.com/iamhssingh)
    """
    from django.contrib.auth import get_user_model
    from django.utils.text import gettext_lazy as _
    from .datatypes import UnixTimestampField

    create_date = UnixTimestampField(_('Create Date'), auto_now_add=True)
    update_date = UnixTimestampField(_('Date Modified'), auto_created=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    class Meta:
        abstract = True
