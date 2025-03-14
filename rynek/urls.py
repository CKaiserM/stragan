from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.StraganView.as_view(), name="home"),
    path('profil/<int:pk>', views.ProfileView.as_view(), name="profile"),
    path('logowanie', views.ProfileView.login_user, name="login"),
    path('wylogowanie', views.ProfileView.logout_user, name="logout"),
    path('aktualizacja-profilu', views.ProfileView.update_user, name="update"),
    path('rejestracja', views.ProfileView.register_user, name="register"),
    path('usun-profil', views.ProfileView.delete_user, name="delete_profile"),

    path('konto-sprzedawcy', views.CompanyProfileView.as_view(), name="copmany_profile"),
    
    path('resetowanie-hasla/', auth_views.PasswordResetView.as_view(template_name="profile/password_reset.html"),name="password_reset"),
    path('potwierdzenie-resetowania-wyslane/', auth_views.PasswordResetDoneView.as_view(template_name="profile/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset-hasla-zakonczony/', auth_views.PasswordResetCompleteView.as_view(template_name="profile/password_reset_complete.html"), name="password_reset_complete"),
    path('zmiana-hasla/', views.ChangePasswordView.as_view(), name='change_password'),

    path('znajdz-produkt/', views.SearchView.as_view(), name='search_product'),
    path('oferta/<slug:slug>/<int:pk>/', views.SingleProductView.as_view(), name='single_product'),
    path('dzial/<slug:slug>/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('kategoria/<slug:slug>/<int:pk>/', views.SubcategoryView.as_view(), name='subcategory'),

]
