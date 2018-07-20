from rest_framework import serializers


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
