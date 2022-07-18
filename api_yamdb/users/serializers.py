from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class VerifyCodeTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name",
            "last_name", "bio", "role"
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError([
                'Не может быть равно me и содержит только латиницу'])
        return value
