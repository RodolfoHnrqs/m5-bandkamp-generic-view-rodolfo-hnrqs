from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "is_superuser"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "is_superuser": {"read_only": True},
            "username": {"validators": [UniqueValidator(queryset=User.objects.all(), message="A user with that username already exists.")]},
            "email": {"validators": [UniqueValidator(queryset=User.objects.all())]}
        }

    def create(self, data):
        return User.objects.create_superuser(**data)
    
    def update(self, instance, data: dict):
        for key, value in data.items():
            if key == "password":
                value = make_password(data[key])
            setattr(instance, key, value)

        instance.save()
        return instance
