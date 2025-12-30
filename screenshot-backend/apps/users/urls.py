from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('info/', views.UserInfoView.as_view(), name='user-info'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('phone/', views.UpdatePhoneView.as_view(), name='update-phone'),
]
