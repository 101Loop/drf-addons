from .db_type import UnixTimestampField, models


class CreateUpdateModel(models.Model):
    from django.utils.text import gettext_lazy as _
    from django.contrib.auth import get_user_model

    create_date = UnixTimestampField(_('Create Date'), auto_now_add=True)
    last_modified = UnixTimestampField(_('Date Modified'), auto_created=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    class Meta:
        abstract = True
