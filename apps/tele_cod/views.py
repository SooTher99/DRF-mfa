from .serializers import SecondFactorSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MFASecondStepJWTView(TokenObtainPairView):
    serializer_class = SecondFactorSerializer


