from django.contrib.auth.models import User

from rest_framework import serializers
from users.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = (
            'id',
            'username',
            'date_joined',
        )
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'last_login',
            'date_joined',
        )

class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Profile
        read_only_fields = (
            'last_active',
            'api_secret',
            'role',
        )
