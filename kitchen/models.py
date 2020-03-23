from decimal import Decimal
from jsonfield import JSONField
from multiselectfield import MultiSelectField

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from utils.models import BaseModel


class Chef(BaseModel):
    DAYS_OF_WEAK_SUNDAY = 'SUNDAY'
    DAYS_OF_WEAK_MONDAY = 'MONDAY'
    DAYS_OF_WEAK_TUESDAY = 'TUESDAY'
    DAYS_OF_WEAK_WEDNESDAY = 'WEDNESDAY'
    DAYS_OF_WEAK_THURSDAY = 'THURSDAY'
    DAYS_OF_WEAK_FRIDAY = 'FRIDAY'
    DAYS_OF_WEAK_SATURDAY = 'SATURDAY'

    DAYS_OF_WEAK_CHOICES = (
        (DAYS_OF_WEAK_SUNDAY, 'Sunday'),
        (DAYS_OF_WEAK_MONDAY, 'Monday'),
        (DAYS_OF_WEAK_TUESDAY, 'Tuesday'),
        (DAYS_OF_WEAK_WEDNESDAY, 'Wednesday'),
        (DAYS_OF_WEAK_THURSDAY, 'Thursday'),
        (DAYS_OF_WEAK_FRIDAY, 'Friday'),
        (DAYS_OF_WEAK_SATURDAY, 'Saturday'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='chefs')
    name = models.CharField(verbose_name='Name', max_length=100, blank=True, null=True)
    description = models.CharField(verbose_name='Description', max_length=250, default='')
    email = models.EmailField('Email address', unique=True)
    phone = models.CharField(verbose_name='Phone', max_length=50, blank=True, null=True)
    address = JSONField(verbose_name='Address', blank=True, null=True, default={})
    open_at = models.TimeField(verbose_name='Open at')
    close_at = models.TimeField(verbose_name='Close at')
    days_of_weak = MultiSelectField(verbose_name='Days of weak', choices=DAYS_OF_WEAK_CHOICES)

    class Meta:
        verbose_name = 'Chef'
        verbose_name_plural = 'Chefs'

    def __str__(self):
        return self.name


class FoodRecipe(BaseModel):

    CATEGORY_OTHERS = 'OTHERS'
    CATEGORY_BRAZILIAN = 'BRAZILIAN'
    CATEGORY_ARABIC = 'ARABIC'
    CATEGORY_ASIAN = 'ASIAN'
    CATEGORY_MEXICAN = 'MEXICAN'
    CATEGORY_ITALIAN = 'ITALIAN'
    CATEGORY_SNACK = 'SCNACK'
    CATEGORY_PACKED_LUNCH = 'PACKED_LUNCH'
    CATEGORY_FIT = 'FIT'
    CATEGORY_MEAT = 'MEAT'
    CATEGORY_PIZZA = 'PIZZA'
    CATEGORY_PASTA = 'PASTA'
    CATEGORY_VEGETARIAN = 'VEGETARIAN'
    CATEGORY_VEGAN = 'VEGAN'
    CATEGORY_DRINK = 'DRINK'

    CATEGORY_CHOICES = (
        (CATEGORY_OTHERS, 'Others'),
        (CATEGORY_BRAZILIAN, 'Brazilian'),
        (CATEGORY_ARABIC, 'Arabic'),
        (CATEGORY_ASIAN, 'Asian'),
        (CATEGORY_MEXICAN, 'Mexican'),
        (CATEGORY_ITALIAN, 'Italian'),
        (CATEGORY_SNACK, 'Snack'),
        (CATEGORY_PACKED_LUNCH, 'Packed lunch'),
        (CATEGORY_MEAT, 'Meat'),
        (CATEGORY_PIZZA, 'Pizza'),
        (CATEGORY_PASTA, 'Pasta'),
        (CATEGORY_FIT, 'Fit'),
        (CATEGORY_VEGETARIAN, 'Vegetarian'),
        (CATEGORY_VEGAN, 'Vegan'),
        (CATEGORY_DRINK, 'Drink'),
    )

    chef = models.ForeignKey('kitchen.Chef', on_delete=models.PROTECT, related_name='food_recipes')
    name = models.CharField(verbose_name='Name', max_length=50, blank=True, null=True)
    description = models.CharField(verbose_name='Description', max_length=250, default='')
    category = models.CharField(verbose_name='Category', max_length=50,
                                choices=CATEGORY_CHOICES, default=CATEGORY_OTHERS)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])
    preparation_time = models.TimeField(verbose_name='Preparation time')

    class Meta:
        verbose_name = 'Food Recipe'
        verbose_name_plural = 'Food Recipes'

    def __str__(self):
        return '{name} - R$ {price}'.format(name=self.name, price=self.price)
