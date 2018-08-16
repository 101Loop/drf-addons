from django.contrib import admin


class CreateUpdateAdmin(admin.ModelAdmin):

    readonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        """
        Makes created_by & create_date readonly when editing.
        """
        if not obj:
            return self.readonly_fields
        return self.readonly_fields + ('created_by', 'create_date')
