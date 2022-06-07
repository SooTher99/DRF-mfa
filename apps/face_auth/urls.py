from django.urls import path
from .views import RegisterApiForThreeFactors

urlpatterns = [
    path('register/', RegisterApiForThreeFactors.as_view()),

]
