from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from utils.helpers import get_address_by_cep, separate_full_name
from utils.serializers import AddressSerializer


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True)
    cep_address = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True)

    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    def get_first_name(self, data):
        first_name, last_name = separate_full_name(data.get('full_name'))
        return first_name

    def get_last_name(self, data):
        first_name, last_name = separate_full_name(data.get('full_name'))
        return last_name
    
    def get_address(self, data):
        return get_address_by_cep(data.get('cep_address'))

    class Meta:
        model = User
        fields = ('full_name', 'password', 'cep_address', 'id', 'first_name', 'last_name', 'email', 'phone', 'address')


class AccountInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    phone = serializers.CharField(required=False)
    address = AddressSerializer(required=False)
    date_joined = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'first_name', 'last_name', 'email', 'phone', 'address',
                  'date_joined', 'last_update')


class AccountChangePasswordSerializer(serializers.Serializer):
    model = User

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.check_password(attrs.get('current_password')):
            raise ValidationError({'current_password': ['Wrong password.']})
        return super().validate(attrs)
