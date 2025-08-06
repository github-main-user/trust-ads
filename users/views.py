from typing import override

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    ChangePasswordSerializer,
    MeSerializer,
    RegisterSerializer,
)

User = get_user_model()


@extend_schema(
    summary="Register a new user",
    description="This endpoint allows anyone to register a new user account.",
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


@extend_schema(
    summary="Retrieve, update or delete current user",
    description="This endpoint allows authenticated users to retrieve, update, or "
    "delete their own user profile.",
)
class MeAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeSerializer
    permission_classes = (IsAuthenticated,)

    @override
    def get_object(self):
        return self.request.user


@extend_schema(
    summary="Change user password",
    description="This endpoint allows authenticated users to change their password.",
)
class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password successfully changed"}, status=status.HTTP_200_OK
        )
