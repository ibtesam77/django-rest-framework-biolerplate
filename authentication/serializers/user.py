from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class VerifyEmailSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('uid', 'token')


class ChangePasswordSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('uid', 'token', 'password')