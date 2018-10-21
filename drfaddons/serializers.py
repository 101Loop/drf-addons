from rest_framework import serializers

from django.utils.text import gettext_lazy as _


class SearchSerializer(serializers.Serializer):
    """
    SearchSerializer is used in various personal projects for query-ing.
    Deprecated now!
    Will be removed in future versions.

    Source: Himanshu Shankar (https://github.com/iamhssingh)
    """
    DeprecationWarning('This class will be removed in future versions. Use Django REST Framework generic API view.')
    listf = ('id', 'create_date', 'last_modified')
    order_by = serializers.ListField(child=serializers.ChoiceField(choices=listf+tuple('-'+x for x in listf)), default=['id'])
    paginator = serializers.IntegerField(default=10)
    page = serializers.IntegerField(default=1)


class ByOwnerSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        model = self.Meta.model

        if model.objects.filter(created_by=self.context['request'].user).count() > 0:
            raise serializers.ValidationError(detail=_('Logged in user already has %s object. Can not create another'
                                                       ' object.' % (model._meta.verbose_name.title())))

        return attrs
