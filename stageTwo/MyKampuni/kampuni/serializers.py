from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from kampuni.models import User, Organization


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                'user_id',
                'first_name',
                'last_name',
                'email',
                'phone'
                ]


class OrganizationSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['org_id', 'name', 'description']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                'first_name',
                'last_name',
                'email',
                'password',
                'phone'
                ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = {
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'email': validated_data.get('email'),
            'password': make_password(validated_data.get('password')),
            'phone': validated_data.get('phone')
            }
        user = User.objects.create(**user_data)
        organization = Organization.objects.create(
            name=f"{user.first_name}'s Organization"
            )
        organization.users.add(user)
        return user
