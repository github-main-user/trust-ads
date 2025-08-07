from typing import override

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.utils import send_reset_password_email

from .serializers import (
    ChangePasswordSerializer,
    MeSerializer,
    RegisterSerializer,
    ResetPasswordConfirmSerializer,
    ResetPasswordRequestSerializer,
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
    responses={200: OpenApiResponse(), 400: OpenApiResponse()},
)
class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)
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


@extend_schema(
    summary="Request user password reset",
    description="This endpoint allows user to request password reset.",
    responses={200: OpenApiResponse()},
)
class ResetPasswordRequestView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        response = Response(
            {"message": "If such an email exists, we sent a letter with instructions"},
            status=status.HTTP_200_OK,
        )

        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
        except User.DoesNotExist:
            return response

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = settings.PASSWORD_RESET_URL.format(uid=uid, token=token)

        send_reset_password_email(user.email, reset_link)

        return response


@extend_schema(
    summary="Confirm user password reset",
    description="This endpoint allows user to confirm password reset.",
    responses={200: OpenApiResponse(), 400: OpenApiResponse()},
)
class ResetPasswordConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data["uid_b64"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(
            user, serializer.validated_data["token"]
        ):
            return Response(
                {"error": "Invalid or outdated token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password successfully reset"}, status=status.HTTP_200_OK
        )
