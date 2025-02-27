from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.StraganView.as_view(), name="home"),
    path('profile/<int:pk>', views.ProfileView.as_view(), name="profile"),
    path('login', views.ProfileView.login_user, name="login"),
    path('logout', views.ProfileView.logout_user, name="logout"),
    path('update', views.ProfileView.update_user, name="update"),
    path('register', views.ProfileView.register_user, name="register"),
    path('delete_profile', views.ProfileView.delete_user, name="delete_profile"),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="profile/password_reset.html"),name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="profile/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="profile/password_reset_complete.html"), name="password_reset_complete"),
    path('password-change/', views.ChangePasswordView.as_view(), name='change_password'),

    path('search_product/', views.SearchView.as_view(), name='search_product'),
]
