from rest_framework import serializers

from kampuni.models import User, Organisation


class UserSerializer(serializers.ModelSerialiser):
    class Meta:
        model = User
        fields = [
                'userId',
                'first_name',
                'last_name',
                'email',
                'phone'
                ]


class OrganizationSerializer(serializers.ModelSerializers):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']


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
        Organisation.objects.create(
                name=f"{user.first_name}'s Organisation",
                users=[user]
                )
        return user
