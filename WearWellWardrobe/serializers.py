from rest_framework import serializers
from WearWellWardrobe.models import Category, Page

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'
