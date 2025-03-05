from rest_framework import serializers
from WearWellWardrobe.models import Category, Page

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    img1 = serializers.SerializerMethodField()  # Convert image field to a full URL

    def get_img1(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img1.url) if obj.img1 else None

    class Meta:
        model = Page
        fields = '__all__'  # Includes all model fields
        
