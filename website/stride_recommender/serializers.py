from rest_framework import serializers

from .models import ContentData

class ContentDataSerializer(serializers.ModelSerializer):
    # anime_url = serializers.HyperlinkedIdentityField('ContentData-list')
    # name = serializers.CharField()
    # image_url = serializers.HyperlinkedIdentityField('ContentData-list')
    # synopsis = serializers.CharField()

    class Meta:
        model = ContentData
        fields = ('anime_url', 'name', 'image_url', 'synopsis', 'studios', 'genres')