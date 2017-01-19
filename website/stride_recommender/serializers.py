from rest_framework import serializers

from .models import ContentData

class ContentDataSerializer(serializers.ModelSerializer):
    name = serializers.HyperlinkedIdentityField('name')
    image_url = serializers.HyperlinkedIdentityField('image_url')
    synopsis = serializers.HyperlinkedIdentityField('synopsis')
    anime_url = serializers.HyperlinkedIdentityField('anime_url')

    class Meta:
        model = ContentData
        fields = ('anime_url', 'name', 'image_url', 'synopsis')