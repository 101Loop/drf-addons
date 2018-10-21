from django.contrib import admin


class CreateUpdateAdmin(admin.ModelAdmin):

    readonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        """
        Makes created_by & create_date readonly when editing.
        """
        fields = list(self.readonly_fields) or []
        if 'created_by' not in fields:
            fields.append('created_by')
        if 'create_date' not in fields:
            fields.append('create_date')
        if 'update_date' not in fields:
            fields.append('update_date')
        return fields

    def save_model(self, request, obj, form, change):
        import datetime

        if change:
            obj.update_date = datetime.datetime.now()
        else:
            obj.created_by = request.user
            obj.create_date = datetime.datetime.now()
        super(CreateUpdateAdmin, self).save_model(request, obj, form, change)


class CreateUpdateHiddenAdmin(CreateUpdateAdmin):
    """
    Hide a model from Application page but allows addition of object from inside of other models.
    """
    def get_model_perms(self, request):
        return {}
