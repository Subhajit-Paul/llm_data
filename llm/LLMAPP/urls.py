from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.landing_page, name="landing"),
    path('home/', views.home_page, name='home'),
    path('details/', views.details1_page, name='details'),
    path('error/', views.error_page, name='error'),
    path('submit_form/', views.submit_form, name='submit_form'),
]