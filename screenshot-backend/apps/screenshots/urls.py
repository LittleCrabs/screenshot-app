from django.urls import path
from . import views

urlpatterns = [
    path('modes/', views.ModeListView.as_view(), name='mode-list'),
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('models/', views.ModelListView.as_view(), name='model-list'),
    path('search/', views.ImageSearchView.as_view(), name='image-search'),
    path('components/', views.ComponentListView.as_view(), name='component-list'),
    path('component-data/', views.ComponentContentView.as_view(), name='component-data'),
    path('videos/', views.VideoListView.as_view(), name='video-list'),
    path('upload-video/', views.VideoUploadView.as_view(), name='upload-video'),
    path('upload-chunk/', views.ChunkUploadView.as_view(), name='upload-chunk'),
    path('merge-chunks/', views.ChunkMergeView.as_view(), name='merge-chunks'),
    path('my-uploads/', views.MyUploadsView.as_view(), name='my-uploads'),
]
