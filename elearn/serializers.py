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


class Values_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Values_Category
        fields = '__all__'

class Values_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Values_SubCategory
        fields = '__all__'


class RecentUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = recent_updates
        fields = '__all__'


class DiffDigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diff_Dig
        fields = '__all__'


class ICardsPDF_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPDF_Category
        fields = '__all__'

class ICardsPDF_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPDF_SubCategory
        fields = '__all__'


class ICardsAudio_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsAudio_Category
        fields = '__all__'

class ICardsAudio_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsAudio_SubCategory
        fields = '__all__'


class ICardsVideo_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideo_Category
        fields = '__all__'

class ICardsVideo_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideo_SubCategory
        fields = '__all__'


class ImageBank_CategorySerializerr(serializers.ModelSerializer):
    class Meta:
        model = ImageBank_Category
        fields = '__all__'

class ImageBank_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBank_SubCategory
        fields = '__all__'


class WallPoster_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  WallPoster_Category
        fields = '__all__'


class WallPoster_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WallPoster_SubCategory
        fields = '__all__'