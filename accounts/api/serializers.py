from django.contrib.auth import get_user_model

from rest_framework import serializers

from accounts.models.profile import Profile
from accounts.models.education import Education

User = get_user_model()


class EducationSerializer(serializers.ModelSerializer):
    """education model serializer"""

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
    """profile model serializer"""

    education = EducationSerializer()

    class Meta:
        model = Profile
        fields = [
            'contact_number',
            'address',
            'education'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    serializer for registering user with valid
    profile and education
    """

    profile = UserProfileSerializer()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Confirm_Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'profile')

    def create(self, validated_data):
        """creating profile and education on creating user"""

        profile_data = validated_data.pop('profile')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        education_data = profile_data.pop('education')
        education = Education.objects.create(**education_data)
        Profile.objects.create(
            user=user,
            contact_number=profile_data['contact_number'],
            address=profile_data['address'],
            education=education
        )
        return user

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError("password doesnot match")
        return data
