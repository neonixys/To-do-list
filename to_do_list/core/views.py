from typing import Any

from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
