from rest_framework import serializers

class StatisticsSerializer(serializers.Serializer):
    axis_labels = serializers.DictField()
    values = serializers.DictField()

class StatisticsListSerializer(serializers.ListSerializer):

    class Meta:
        list_serializer_class = StatisticsSerializer