from rest_framework import serializers

class StatisticsSerializer(serializers.Serializer):
    axis_labels = serializers.CharField(max_length='500')
    values = serializers.CharField(max_length='500')

class StatisticsListSerializer(serializers.ListSerializer):

    class Meta:
        list_serializer_class = StatisticsSerializer