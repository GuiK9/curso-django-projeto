from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),  # Home
    path('recipe/<int:id>/', views.recipe),  # Recipe

]
