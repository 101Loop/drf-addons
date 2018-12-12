"""
Custom serializers

Author: Himanshu Shankar (https://himanshus.com)
"""

from rest_framework import serializers

from django.utils.text import gettext_lazy as _


class ByOwnerSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        model = self.Meta.model

        if model.objects.filter(
                created_by=self.context['request'].user).count() > 0:
            raise serializers.ValidationError(
                detail=_('Logged in user already has %s object.'
                         'Can not create another object.' % (
                    model._meta.verbose_name.title())))

        return attrs
