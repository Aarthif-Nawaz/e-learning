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


class DailyBoosterMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoosterMain
        fields = '__all__'


class DailyBoostBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoostBanner
        fields = '__all__'


class DailyBoosterQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoosterQuiz
        fields = '__all__'


class DailyBoosterQuizTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoosterQuizTimer
        fields = '__all__'


class DailyBoosterQuizCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoosterCompleted
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


class PrimeClassVideo_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassVideo_Category
        fields = '__all__'


class PrimeClassVideo_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassVideo_SubCategory
        fields = '__all__'


class PrimeClassVideo_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassVideo
        fields = '__all__'


class PrimeClassAudio_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassAudio_Category
        fields = '__all__'


class PrimeClassAudio_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassAudio_SubCategory
        fields = '__all__'


class PrimeClassAudio_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassAudio
        fields = '__all__'


class PrimeClassNotes_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassNotes_Category
        fields = '__all__'


class PrimeClassNotes_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassNotes_SubCategory
        fields = '__all__'


class PrimeClassNotes_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassNotes
        fields = '__all__'

    # ----------------Live class  13 july ---


class LiveClassBannerImage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClassBannerImage
        fields = '__all__'


class LiveClass_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass_Category
        fields = '__all__'


class LiveClass_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass_SubCategory
        fields = '__all__'


class LiveClass_Serializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass
        fields = '__all__'


# --------------- QuestionBankPreviousQuestions

class QuestionBankPreviousQuestions_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBankPreviousQuestions_Category
        fields = '__all__'


class QuestionBankPreviousQuestions_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBankPreviousQuestions_SubCategory
        fields = '__all__'


class QuestionBankPreviousQuestions_Serializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBankPreviousQuestions
        fields = '__all__'


class QuestionDiscussion_Serializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionDiscussion
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'mobile', 'email', 'college', 'location')


class UserBlockedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_blocked',)


class QuestionBankTestModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBankTestMode
        fields = '_all_'


class QuestionBankModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBankMode
        fields = '_all_'


class QuestionBankQuizTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBankQuizTimer
        fields = '_all_'


class QuestionBankCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBankCompleted
        fields = '_all_'


class ShotsbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ShotsbookMark
        fields = '_all_'


class ShotsLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ShotsLiked
        fields = '_all_'


class Diff_DigbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Diff_DigbookMark
        fields = '_all_'


class Diff_DigLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Diff_DigLiked
        fields = '_all_'


class Recent_UpdatesbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Recent_UpdatesbookMark
        fields = '_all_'


class Recent_UpdatesLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Recent_UpdatesLiked
        fields = '_all_'


class ValuesbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ValuesbookMark
        fields = '_all_'


class ValuesLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ValuesLiked
        fields = '_all_'


class ICardsPDFbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPDFbookMark
        fields = '_all_'


class ICardsPDFLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPDFLiked
        fields = '_all_'


class ICardsAudiobookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsAudiobookMark
        fields = '_all_'


class ICardsAudioLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsAudioLiked
        fields = '_all_'


class ICardsVideobookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideobookMark
        fields = '_all_'


class ICardsVideoLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsVideoLiked
        fields = '_all_'


class ImageBankbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBankbookMark
        fields = '_all_'


class ImageBankLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBankLiked
        fields = '_all_'


class WallPostersbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = WallPostersbookMark
        fields = '_all_'


class WallPostersLiked_Serializer(serializers.ModelSerializer):
    class Meta:
        model = WallPostersLiked
        fields = '_all_'


# ---------- only bookmark
class PrimeClassVideobookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassVideobookMark
        fields = '_all_'


class PrimeClassAudiobookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassAudiobookMark
        fields = '_all_'


class PrimeClassNotesbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeClassNotesbookMark
        fields = '_all_'


class LiveClassbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClassbookMark
        fields = '_all_'


class QuestionDiscussionbookMark_Serializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionDiscussionbookMark
        fields = '_all_'

class ICardsPastPaper_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPastPaper_Category
        fields = ('name', )

class ICardsPastPaper_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPastPaper_SubCategory
        fields = ('category', 'name')

class ICardsPastPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICardsPastPaper
        fields = ('sub_category', 'title', 'pdf')


class Test_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_Category
        fields = '_all_'


class Test_SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_SubCategory
        fields = '_all_'


class TestQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestions
        fields = '_all_'


class TestQuestionStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestionStatistics
        fields = '_all_'


class TestQuestionDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestionStatistics
        fields = '_all_'


class TestDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestDiscussion
        fields = '_all_'


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '_all_'


class GroupDiscussionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDiscussionAdmin
        fields = ('groupname', 'image')


class GroupDiscussionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDiscussionUser
        fields = '_all_'


class DailyBoosterBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoosterBookMark
        fields = '_all_'


class LeaderBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderBoard
        fields = '_all_'