from .serializers import FirstFactorSerializer, DefaultFactorSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class RegisterApiDefault(GenericAPIView):
    serializer_class = DefaultFactorSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User Created Successfully.",},  status=status.HTTP_201_CREATED)


class MFAFirstStepJWTView(TokenObtainPairView):
    serializer_class = FirstFactorSerializer
