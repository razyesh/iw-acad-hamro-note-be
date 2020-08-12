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
            'education',
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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
            'profile'
        )

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
            raise serializers.ValidationError("password doesn't match")
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    serializer for updating user with valid
    profile and education
    """

    profile = UserProfileSerializer()
    profile_pic = serializers.FileField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_pic', 'profile')

    def update(self, instance, validated_data):
        """updating profile and education while updating user"""
        profile_data = validated_data.pop('profile')
        education_data = profile_data.pop('education')
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        profile_instance = Profile.objects.get(user=instance)
        profile_instance.contact_number = profile_data['contact_number']
        profile_instance.address = profile_data['address']
        profile_instance.profile_pic = validated_data['profile_pic']
        profile_instance.education.semester = education_data['semester']
        profile_instance.education.year = education_data['year']
        profile_instance.education.faculty = education_data['faculty']
        profile_instance.education.university = education_data['university']
        profile_instance.education.college = education_data['college']
        profile_instance.save()
        instance.save()
        return instance
