from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import MFASecondStepJWTView


urlpatterns = [
    path('login/code/', MFASecondStepJWTView.as_view(), name='token_login_second'),
]

