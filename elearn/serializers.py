from rest_framework import serializers
from elearn.models import *


class ShotsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShotsCategory
        fields = '__all__'


class ShotsSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShotsSubCategory
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


class ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Values
        fields = '__all__'


class Recent_Updates_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent_Updates_Category
        fields = '__all__'


class Recent_Updates_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent_Updates_SubCategory
        fields = '__all__'


class RecentUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = recent_updates
        fields = '__all__'


class Diff_Dig_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diff_Dig_Category
        fields = '__all__'


class Diff_Dig_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diff_Dig_SubCategory
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


class ICardsPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPDF
        fields = '__all__'


class ICardsAudio_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsAudio_Category
        fields = '__all__'


class ICardsAudio_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsAudio_SubCategory
        fields = '__all__'


class ICardsAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsAudio
        fields = '__all__'


class ICardsVideo_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideo_Category
        fields = '__all__'


class ICardsVideo_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideo_SubCategory
        fields = '__all__'


class ICardsVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideo
        fields = '__all__'


class ImageBank_CategorySerializerr(serializers.ModelSerializer):
    class Meta:
        model = ImageBank_Category
        fields = '__all__'


class ImageBank_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBank_SubCategory
        fields = '__all__'


class ImageBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBank
        fields = '__all__'


class WallPoster_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WallPoster_Category
        fields = '__all__'


class WallPoster_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WallPoster_SubCategory
        fields = '__all__'


class WallPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WallPosters
        fields = '__all__'


class QuestionOfTheDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOfTheDay
        fields = '__all__'


class DailyBoostBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoostBanner
        fields = '__all__'


class DailyBoosterQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoosterQuiz
        fields = '__all__'


class QuestionBank_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank_Category
        fields = '__all__'


class QuestionBank_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank_SubCategory
        fields = '__all__'


class QuestionBank_Serializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = '__all__'
