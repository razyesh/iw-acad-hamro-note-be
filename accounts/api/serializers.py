from django.contrib.auth import get_user_model

from rest_framework import serializers

from accounts.models.profile import Profile
from accounts.models.education import Education

User = get_user_model()


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'semester',
            'year',
            'college',
            'faculty',
            'university'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer()

    class Meta:
        model = Profile
        fields = [
            'contact_number',
            'address',
            'education'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        education_data = profile_data.pop('education')
        education = Education.objects.create(**education_data)
        Profile.objects.create(
            user=user,
            contact_number=profile_data['contact_number'],
            address=profile_data['address'],
            education=education
        )
        return user
