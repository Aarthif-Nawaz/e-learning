from django.urls import path
from elearn.views import *

urlpatterns = [
    path('shots/', ShotsView.as_view(), name="shots register"),
    path('category/', CategoryView.as_view(), name="category register"),
    path('sub_category/', SubCategoryView.as_view(), name="sub category register"),
    path('recent_updates/', RecentUpdatesView.as_view(), name="Recent Updates register"),
    path('values/', Values_CategoryView.as_view(), name="Values register"),
    path('diff_dig/', Diff_DigView.as_view(), name="Diff Dig register"),
    path('icards_pdf/', ICardsPDF_CategoryView.as_view(), name="Icards PDF register"),
    path('icards_video/', ICardsVideo_CategoryView.as_view(), name="Icards Video register"),
    path('icards_audio/', ICardsAudio_CategoryView.as_view(), name="Icards Audio register"),
    path('image_bank/', ImageBank_CategoryView.as_view(), name="Icards Video register"),
    path('wall_poster/', WallPoster_CategoryView.as_view(), name="Icards Video register"),
    path('DailyBoostBanner/', DailyBoostBannerView.as_view(), name="DailyBoostBanner"),
    path('QuestionOfTheDay/', QuestionOfTheDayView.as_view(), name="QuestionOfTheDayView"),

    path('DailyBoosterQuiz/', DailyBoosterQuizView.as_view(), name="DailyBoosterQuizView"),
    path('QuestionBank_Category/', QuestionBank_CategoryView.as_view(), name="QuestionBank_CategoryView"),
    path('QuestionBank_SubCategory/', QuestionBank_SubCategoryView.as_view(), name="QuestionBank_SubCategoryView"),
  



]
