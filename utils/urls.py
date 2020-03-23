from django.urls import include, path

from . import views as utils_views


urlpatterns = [
    path('address/<cep>/', utils_views.AddressByCepView.as_view()),
]
