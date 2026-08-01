from django.urls import path
from . import views
from . import utils

urlpatterns = [
  path('register/', views.registeruser, name='register'),

  path('login/', views.login, name='login'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('logout/', views.logout, name='logout'),
 


  path('activate/<uidb64>/<token>/', views.activate, name='activate'),

  path('resetpasswordvalidate/<uidb64>/<token>/', views.resetpasswordvalidate, name='resetpasswordvalidate'),
  path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
  path('resetpassword/', views.resetpassword, name='resetpassword'),


]

