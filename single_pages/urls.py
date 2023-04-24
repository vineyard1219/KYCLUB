from django.urls import path
from . import views

urlpatterns = [
    path('about_me/', views.about_me),
    path('about_me2/', views.about_me2),
    path('', views.landing),
]