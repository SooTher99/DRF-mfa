from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import RegisterApi, MFAFirstStepJWTView


urlpatterns = [
    path('register/', RegisterApi.as_view(), name='registration'),
    path('login/', MFAFirstStepJWTView.as_view(), name='token_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

