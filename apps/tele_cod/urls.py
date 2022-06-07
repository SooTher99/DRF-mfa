from .views import MFASecondStepJWTView, RegisterApiForTwoFactors

from django.urls import path



urlpatterns = [
    # path('register/', RegisterApiForTwoFactors.as_view(), name='token_login_second'),
    path('login/code/', MFASecondStepJWTView.as_view(), name='token_login_second'),
]

