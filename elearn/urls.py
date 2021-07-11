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

]
