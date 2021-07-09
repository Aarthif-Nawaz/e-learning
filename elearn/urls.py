from django.urls import path
from elearn.views import *

urlpatterns = [
    path('shots/', ShotsView.as_view(), name="shots register"),
    path('category/', CategoryView.as_view(), name="category register"),
    path('sub_category/', SubCategoryView.as_view(), name="sub category register"),
    path('recent_updates/', RecentUpdatesView.as_view(), name="Recent Updates register"),
    path('values/', ValuesView.as_view(), name="Values register"),
    path('diff_dig/', Diff_DigView.as_view(), name="Diff Dig register"),
    path('icards_pdf/', ICardsPDFView.as_view(), name="Icards PDF register"),
    path('icards_video/', ICardsVideoView.as_view(), name="Icards Video register"),
    path('image_bank/', ImageBankView.as_view(), name="Icards Video register"),
    path('wall_poster/', WallPosterView.as_view(), name="Icards Video register"),

]
