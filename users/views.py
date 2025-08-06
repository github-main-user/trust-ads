from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import MeSerializer, RegisterSerializer


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

    def get_object(self):
        return self.request.user
