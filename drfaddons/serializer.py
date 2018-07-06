from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    This filter only allows users to see their own object
    Source: http://www.django-rest-framework.org/api-guide/filtering/
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(created_by=request.user)


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
