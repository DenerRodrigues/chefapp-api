from django.urls import include, path

from . import views as kitchen_views


urlpatterns = [
    path('chef/', kitchen_views.ChefListCreateView.as_view()),
    path('chef/<id>/', kitchen_views.ChefRetrieveUpdateDestroyView.as_view()),
    path('chef/<chef_id>/foodrecipe/', kitchen_views.FoodRecipeListCreateView.as_view()),
    path('chef/<chef_id>/foodrecipe/<id>/', kitchen_views.FoodRecipeRetrieveUpdateDestroyView.as_view()),

    path('public/chef/', kitchen_views.ChefPublicListView.as_view()),
    path('public/foodrecipe/', kitchen_views.FoodRecipePublicListView.as_view()),
    path('public/foodrecipe/category/', kitchen_views.FoodRecipeCategoryListView.as_view())
]
