from rest_framework import serializers
from api.models import User
import jwt
import bcrypt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "password")

    def validate(self, attr):
        attr["email"] = attr["email"].lower()
        attr["password"] = bcrypt.hashpw(
            attr["password"].encode(), bcrypt.gensalt(rounds=10)
        ).decode()
        return super().validate(attr)


class UpdateUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=128, required=False)

    def validate(self, attrs):
        if "password" in attrs:
            attrs["password"] = bcrypt.hashpw(
                attrs["password"].encode(), bcrypt.gensalt(rounds=10)
            ).decode()
        return super().validate(attrs)


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email")
