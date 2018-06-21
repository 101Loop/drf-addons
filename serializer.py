from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend


class IsOwnerFilterBackend(BaseFilterBackend):
    """
    This filter only allows users to see their own object
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(created_by=request.user)


class SearchSerializer(serializers.Serializer):
    listf = ('id', 'create_date', 'last_modified')
    order_by = serializers.ListField(child=serializers.ChoiceField(choices=listf+tuple('-'+x for x in listf)), default=['id'])
    paginator = serializers.IntegerField(default=10)
    page = serializers.IntegerField(default=1)
