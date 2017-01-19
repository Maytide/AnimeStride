from rest_framework import viewsets

from .models import ContentData
from .serializers import ContentDataSerializer

class ContentDataViewSet(viewsets.ModelViewSet):
    queryset = ContentData.objects.all().order_by('name')
    serialzier_class = ContentDataSerializer