from django.urls import path
from elearn.views import *

urlpatterns = [
    path('shots/', ShotsView.as_view(), name="shots register"),
    path('shots_category/', ShotsCategoryView.as_view(), name="shots category register"),
    path('shots_sub_category/', ShotsSubCategoryView.as_view(), name="shots sub category register"),
    path('recent_updates/', RecentUpdatesView.as_view(), name="Recent Updates register"),
    path('recent_updates_category/', RecentUpdatesCategoryView.as_view(), name="Recent Updates category register"),
    path('recent_updates_subCategory/', RecentUpdatesSubCategoryView.as_view(), name="Recent Updates sub category register"),
    path('values_category/', Values_CategoryView.as_view(), name="values category register"),
    path('values_sub_category/', Values_SubCategoryView.as_view(), name="values sub category register"),
    path('values/', ValuesView.as_view(), name="Values register"),
    path('diff_dig_category/', Diff_Dig_CategoryView.as_view(), name="diff dig category register"),
    path('diff_dig_sub_category/', Diff_Dig_SubCategoryView.as_view(), name="diff dig sub category register"),
    path('diff_dig/', Diff_DigView.as_view(), name="Diff Dig register"),
    path('icards_pdf_category/', ICardsPDF_CategoryView.as_view(), name="icards pdf category register"),
    path('icards_pdf_sub_category/', ICardsPDF_SubCategoryView.as_view(), name="icards pdf sub category register"),
    path('icards_pdf/', ICardsPDFView.as_view(), name="Icards PDF register"),
    path('icards_video_category/', ICardsVideo_CategoryView.as_view(), name="icards video category register"),
    path('icards_video_sub_category/', ICardsVideo_SubCategoryView.as_view(), name="icards video sub category register"),
    path('icards_video/', ICardsVideoView.as_view(), name="Icards Video register"),
    path('icards_audio_shots_category/', ICardsAudio_CategoryView.as_view(), name="icards audio category register"),
    path('icards_audio_sub_category/', ICardsAudio_SubCategoryView.as_view(), name="icards audio sub category register"),
    path('icards_audio/', ICardsAudioView.as_view(), name="Icards Audio register"),
    path('image_bank_category/', ImageBank_CategoryView.as_view(), name="image bank category register"),
    path('image_bank_sub_category/', ImageBank_SubCategoryView.as_view(), name="image bank sub category register"),
    path('image_bank/', ImageBankView.as_view(), name="Image Bank register"),
    path('wall_poster_category/', WallPoster_CategoryView.as_view(), name="wall poster category register"),
    path('wall_poster_sub_category/', WallPoster_SubCategoryView.as_view(), name="wall poster sub category register"),
    path('wall_poster/', WallPosterView.as_view(), name="wall poster register"),
    path('DailyBoostBanner/', DailyBoostBannerView.as_view(), name="DailyBoostBanner"),
    path('QuestionOfTheDay/', QuestionOfTheDayView.as_view(), name="QuestionOfTheDayView"),
    path('DailyBoosterQuiz/', DailyBoosterQuizView.as_view(), name="DailyBoosterQuizView"),
    path('QuestionBank_Category/', QuestionBank_CategoryView.as_view(), name="QuestionBank_CategoryView"),
    path('QuestionBank_SubCategory/', QuestionBank_SubCategoryView.as_view(), name="QuestionBank_SubCategoryView"),
    path('QuestionBank/', QuestionBankView.as_view(), name="QuestionBankView"),


    path('PrimeClassVideo_Category/', PrimeClassVideo_CategoryView.as_view(), name="PrimeClassVideo_CategoryView"),
    path('PrimeClassVideo_SubCategory/', PrimeClassVideo_SubCategoryView.as_view(), name="PrimeClassVideo_SubCategoryView"),
    path('PrimeClassVideo/', PrimeClassVideoView.as_view(), name="PrimeClassVideoView"),

    path('PrimeClassAudio_Category/', PrimeClassAudio_CategoryView.as_view(), name="PrimeClassAudio_CategoryView"),
    path('PrimeClassAudio_SubCategory/', PrimeClassAudio_SubCategoryView.as_view(), name="PrimeClassAudioSubCategoryView"),
    path('PrimeClassAudio/', PrimeClassAudioView.as_view(), name="PrimeClassAudioView"),

    path('PrimeClassNotes_Category/', PrimeClassNotes_CategoryView.as_view(), name="PrimeClassNotes_CategoryView"),
    path('PrimeClassNotes_SubCategory/', PrimeClassNotes_SubCategoryView.as_view(), name="PrimeClassNotes_SubCategoryView"),
    path('PrimeClassNotes/', PrimeClassNotesView.as_view(), name="PrimeClassNotesView"),

    path('LiveClassBannerImage/', LiveClassBannerImageView.as_view(), name="LiveClassBannerImageView"),
    path('LiveClass_Category/', LiveClass_CategoryView.as_view(), name="LiveClass_CategoryView"),
    path('LiveClass_SubCategory/', LiveClass_SubCategoryView.as_view(), name="LiveClass_SubCategoryView"),
    path('LiveClass/', LiveClassView.as_view(), name="LiveClassView"),


    path('QuestionBankPreviousQuestions_Category/', QuestionBankPreviousQuestions_CategoryView.as_view(), name="QuestionBankPreviousQuestions_CategoryView"),
    path('QuestionBankPreviousQuestions_SubCategory/', QuestionBankPreviousQuestions_SubCategoryView.as_view(), name="QuestionBankPreviousQuestions_SubCategoryView"),
    path('QuestionBankPreviousQuestions/', QuestionBankPreviousQuestionsView.as_view(), name="QuestionBankPreviousQuestionsView"),

    path('QuestionDiscussion/', QuestionDiscussionView.as_view(), name="QuestionDiscussionView"),

]
