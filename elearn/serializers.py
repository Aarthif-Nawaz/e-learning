from rest_framework import serializers
from elearn.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shots
        fields = '__all__'


class ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Values
        fields = '__all__'


class RecentUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = recent_updates
        fields = '__all__'


class DiffDigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diff_Dig
        fields = '__all__'


class ICardsPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPDF
        fields = '__all__'


class ICardsVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideo
        fields = '__all__'


class ImageBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBank
        fields = '__all__'


class WallPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WallPosters
        fields = '__all__'
