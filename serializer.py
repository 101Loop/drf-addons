from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    listf = ('id', 'create_date', 'last_modified')
    order_by = serializers.ListField(child=serializers.ChoiceField(choices=listf+tuple('-'+x for x in listf)), default=['create_date'])
    paginator = serializers.IntegerField(default=10)
    page = serializers.IntegerField(default=1)
