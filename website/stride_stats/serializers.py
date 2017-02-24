from rest_framework import serializers

from .models import ContentData, BasicStatistics, ItemRecs
# from ..stride_recommender.serializers import ContentDataSerializer


class StatisticsSerializer(serializers.Serializer):
    axis_labels = serializers.DictField()
    values = serializers.DictField()

class StatisticsListSerializer(serializers.ListSerializer):

    class Meta:
        list_serializer_class = StatisticsSerializer

class ContentDataSerializer(serializers.ModelSerializer):
    # anime_url = serializers.HyperlinkedIdentityField('ContentData-list')
    # name = serializers.CharField()
    # image_url = serializers.HyperlinkedIdentityField('ContentData-list')
    # synopsis = serializers.CharField()

    class Meta:
        model = ContentData
        # fields = ('anime_url', 'name', 'image_url', 'synopsis', 'studios', 'genres', 'media', 'members', 'aired', 'episodes', 'score')
        fields = '__all__'

class BasicStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicStatistics
        fields = '__all__'


class ItemRecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRecs
        fields = '__all__'