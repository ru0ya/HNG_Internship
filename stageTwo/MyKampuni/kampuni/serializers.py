from rest_framework import serializers

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

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        organization = Organization.objects.create(
                name=f"{user.first_name}'s Organisation",
                )
        organization.users.add(user)

        return user
