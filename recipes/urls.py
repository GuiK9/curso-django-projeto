from django.urls import path
from . import views

# recipes:recipe
app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewBase.as_view(), name="home"),  # Home
    path('recipes/search/', views.search, name="search"),  # url
    path('recipes/category/<int:category_id>/', views.category, name="category"),  # category
    path('recipes/<int:id>/', views.recipe, name="recipe"),  # Recipe

]
