from rest_framework import serializers

from .models import ContentData, BasicStatistics, ItemRecs
# from ..stride_recommender.serializers import ContentDataSerializer


class StatisticsSerializer(serializers.Serializer):
    axis_labels = serializers.DictField()
    values = serializers.DictField()

# class StatisticsListSerializer(serializers.ListSerializer):
#
#     class Meta:
#         list_serializer_class = StatisticsSerializer

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
    # Serialize modified version of model:
    # http://stackoverflow.com/questions/14583816/django-rest-framework-how-to-add-custom-field-in-modelserializer
    rating_hist = serializers.ListField(source='get_rating_hist')

    class Meta:
        model = BasicStatistics
        # fields = '__all__'
        fields = ('show_name', 'mean', 'var', 'std', 'rating_hist')
        read_only_fields = ('rating_hist',)


class ItemRecsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='show_name')
    # rec_1 = ContentDataSerializer()
    # rec_2 = ContentDataSerializer()
    # rec_3 = ContentDataSerializer()
    # rec_4 = ContentDataSerializer()
    # rec_5 = ContentDataSerializer()
    # rec_6 = ContentDataSerializer(source='rec_6')

    class Meta:
        model = ItemRecs
        fields = ('show_name', 'rec_1', 'rec_2', 'rec_3', 'rec_4', 'rec_5', 'rec_6')