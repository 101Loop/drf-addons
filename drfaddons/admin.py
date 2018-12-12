"""
Admin interfacing for CreateUpdate Model
Contains various classes that inherits from admin.ModelAdmin
CreateUpdateAdmin: Admin class for models extending CreateUpdateModel
HideModelAdminMixin: Mixin that hides a model from admin but allows
                    it's access from inside of another form
CreateUpdateHiddenAdmin: CreateUpdateAdmin with HideModelAdminMixin
InlineCreateUpdateAdminMixin: Takes care of inline formset where model
                            inherits CreateUpdateModel and has those
                            fields as readonly.

Author: Himanshu Shankar (https://himanshus.com)
"""

from django.contrib import admin


class HideModelAdminMixin:
    """
    Hide a model from Application page but allows addition of object
    from inside of other models.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    def get_model_perms(self, request):
        return {}


class InlineCreateUpdateAdminMixin:
    """
    An Inline mixin that takes care of CreateUpdateModel fields.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    def save_formset(self, request, form, formset, change):
        # Check if created_by is in excluded fields
        # Even if created_by is in field, we only need to pick current
        # user when the field is excluded. If it's not excluded, admin
        # may want to setup created_by manually.
        if 'created_by' in formset.form.Meta.exclude:
            # Perform non-commit save to get objects in formset
            formset.save(commit=False)

            # Check if any new object is being created
            if hasattr(formset, 'new_objects'):
                for new_object in formset.new_objects:
                    new_object.created_by = request.user

        # Finally, call super function to save object.
        super(InlineCreateUpdateAdminMixin, self).save_formset(request=request,
                                                               form=form,
                                                               formset=formset,
                                                               change=change)


class CreateUpdateAdmin(InlineCreateUpdateAdminMixin, admin.ModelAdmin):
    """
    An Admin interface for models using CreateUpdateModel.
    Sets `created_by`, `create_date`, & `update_date` to readonly.
    If `created_by` is readonly in the form, it sets its value to
    current logged in user.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    readonly_fields = ()

    # Define ownership_info for common attributes across all models
    ownership_info = {
        'label': 'Ownership Info',
        'fields': {
            'created_by': {'readonly': True},
            'create_date': {'readonly': True},
            'update_date': {'readonly': True}
        }
    }

    def get_fieldsets(self, request, obj=None):
        """
        Add ownership info fields in fieldset with proper separation.

        Author: Himanshu Shankar (https://himanshus.com)
        """
        fieldsets = list(super(CreateUpdateAdmin, self).get_fieldsets(
            request=request, obj=obj))

        # Create sets for future use
        fields = set()
        to_add = set()

        # Prepare a set of existing fields in fieldset
        for fs in fieldsets:
            fields = fields.union(fs[1]['fields'])

        # Loop over ownership info fields
        for k, v in self.ownership_info['fields'].items():

            # Check if current model has k attribute
            # and field k is not already in fieldset
            # and field k has not been excluded
            if (hasattr(self.model, k)
                    and k not in fields
                    and k not in self.exclude):

                # Now, let's hide fields in add form, it will be empty
                # Check if readonly property is not True
                # or this is an edit form
                if ('readonly' in v and not v['readonly']) or obj:
                    to_add.add(k)

        # If to_add set is not empty, add ownership info to fieldset
        if len(to_add) > 0:
            fieldsets.append((self.ownership_info['label'],
                              {'fields': tuple(to_add)}))
        return tuple(fieldsets)

    def get_readonly_fields(self, request, obj=None):
        """
        Makes `created_by`, `create_date` & `update_date` readonly when
        editing.

        Author: Himanshu Shankar (https://himanshus.com)
        """

        # Get read only fields from super
        fields = list(super(CreateUpdateAdmin, self).get_readonly_fields(
            request=request, obj=obj))

        # Loop over ownership info field
        for k, v in self.ownership_info['fields'].items():

            # Check if model jas k attribute
            # and field k is readonly
            # and k is not already in fields
            # and k is not in excluded field
            # (if not checked, form.Meta.exclude has same field twice)
            if (hasattr(self.model, k)
                    and ('readonly' in v and v['readonly'])
                    and k not in fields
                    and k not in self.exclude):
                fields.append(k)
        return tuple(fields)

    def save_model(self, request, obj, form, change):
        # Check if `created_by` has been excluded and the form is for
        # creating a new object.
        if 'created_by' in form.Meta.exclude and not change:
            # Set created_by to current user
            obj.created_by = request.user

        # Finally, call super
        super(CreateUpdateAdmin, self).save_model(request=request, obj=obj,
                                                  form=form, change=change)


class CreateUpdateHiddenAdmin(HideModelAdminMixin, CreateUpdateAdmin):
    """
    Hidden mode of CreateUpdateAdmin

    Author: Himanshu Shankar (https://himanshus.com)
    """
    pass
