from decimal import Decimal

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from .models import Chef, FoodRecipe
from utils.helpers import get_address_by_cep
from utils.serializers import AddressSerializer


class ChefCreateListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    email = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Chef.objects.all())])
    phone = serializers.CharField(required=True)
    cep_address = serializers.CharField(required=True, write_only=True)
    open_at = serializers.TimeField(required=True)
    close_at = serializers.TimeField(required=True)
    days_of_weak = serializers.MultipleChoiceField(required=True, choices=Chef.DAYS_OF_WEAK_CHOICES)
    date_joined = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

    address = serializers.SerializerMethodField()
    
    def get_address(self, data):
        if isinstance(data, dict) and data.get('cep_address'):
            return get_address_by_cep(data.get('cep_address'))
        return data.address

    class Meta:
        model = Chef
        fields = ('cep_address', 'id', 'name', 'description', 'email', 'phone', 'address',
                  'open_at', 'close_at', 'days_of_weak', 'date_joined', 'last_update')


class ChefRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    email = serializers.CharField(required=False, validators=[UniqueValidator(queryset=Chef.objects.all())])
    phone = serializers.CharField(required=False)
    address = AddressSerializer(required=False)
    open_at = serializers.TimeField(required=False)
    close_at = serializers.TimeField(required=False)
    days_of_weak = serializers.MultipleChoiceField(required=False, choices=Chef.DAYS_OF_WEAK_CHOICES)
    date_joined = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chef
        fields = ('id', 'name', 'description', 'email', 'phone', 'address',
                  'open_at', 'close_at', 'days_of_weak', 'date_joined', 'last_update')


class FoodRecipeListCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    chef = ChefRetrieveUpdateDestroySerializer(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    category = serializers.ChoiceField(required=False, choices=FoodRecipe.CATEGORY_CHOICES)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    preparation_time = serializers.TimeField(required=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        chefs = self.context.get('request').user.chefs
        if not chefs.filter(id=self.context.get('view').kwargs.get('chef_id')):
            raise exceptions.NotFound('Chef not found.')
        return super().validate(attrs)

    class Meta:
        model = FoodRecipe
        fields = ('id', 'name', 'description', 'category', 'price', 'preparation_time',
                  'date_joined', 'last_update', 'chef')


class FoodRecipeRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    chef = ChefRetrieveUpdateDestroySerializer(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    category = serializers.ChoiceField(required=False, choices=FoodRecipe.CATEGORY_CHOICES)
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    preparation_time = serializers.TimeField(required=False)
    date_joined = serializers.DateTimeField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        chefs = self.context.get('request').user.chefs
        if not chefs.filter(id=self.context.get('view').kwargs.get('chef_id')):
            raise exceptions.NotFound('Chef not found.')
        return super().validate(attrs)

    class Meta:
        model = FoodRecipe
        fields = ('id', 'name', 'description', 'category', 'price', 'preparation_time',
                  'date_joined', 'last_update', 'chef')
