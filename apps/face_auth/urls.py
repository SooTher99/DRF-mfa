from django.urls import path
from .views import RegisterApiForThreeFactors, FaceAuthJWTView

urlpatterns = [
    path('register/', RegisterApiForThreeFactors.as_view()),
    path('login/code/face/', FaceAuthJWTView.as_view()),

]
