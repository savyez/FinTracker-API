from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginTokenObtainPairSerializer, RegisterSerializer


# Register View to handle user registration
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Success! User registered successfully.",
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email
            }}, status=status.HTTP_201_CREATED)
    


class UserLoginTokenView(TokenObtainPairView):
    serializer_class = LoginTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "error": "GET method not allowed. Use POST to obtain token."
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({
                "error": "Invalid username or password",
                "details": str(e)
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            "message": "Success! Token generated successfully.",
            "data": {
                "username": LoginTokenObtainPairSerializer.get_token(serializer.user)['username'],
                "access_token": serializer.validated_data['access'],
                "refresh_token": serializer.validated_data['refresh']
                }}, status=status.HTTP_200_OK)


class RefreshTokenView(TokenObtainPairView):
    serializer_class = LoginTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({
                "error": "Invalid refresh token",
                "details": str(e)
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            "message": "Success! Token refreshed successfully.",
            "data": {
                "username": LoginTokenObtainPairSerializer.get_token(serializer.user)['username'], 
                "access_token": serializer.validated_data['access'],
                "refresh_token": serializer.validated_data['refresh']
                }}, status=status.HTTP_200_OK)