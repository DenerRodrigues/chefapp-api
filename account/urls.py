from django.urls import include, path

from . import views as account_views


urlpatterns = [
    path('signup/', account_views.SignUpView.as_view()),
    path('account/info/', account_views.AccountInfoView.as_view()),
    path('account/change_password/', account_views.AccountChangePasswordView.as_view()),
]
