from django.urls import path
from . import views

urlpatterns = [
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('models/', views.ModelListView.as_view(), name='model-list'),
    path('versions/', views.VersionListView.as_view(), name='version-list'),
    path('search/', views.ImageSearchView.as_view(), name='image-search'),
]
