from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')

        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def validate_password(self, value: str) -> str:
        return make_password(value)


class ObtainTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = dict(super().validate(attrs))
        del data['refresh']
        return data
