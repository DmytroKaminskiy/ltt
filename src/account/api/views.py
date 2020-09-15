from account.api import serializers

from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class UsersView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny, )

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # add token
        refresh = self.get_token(serializer.instance)
        data = dict(serializer.data)  # serializer.data is immutable
        data['access'] = str(refresh.access_token)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class TokenObtainView(TokenObtainPairView):
    serializer_class = serializers.ObtainTokenSerializer
