from django.contrib import admin

from .models import Chef, FoodRecipe


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'owner', 'is_active', 'date_joined',]
    list_filter = ['is_active',]
    search_fields = ['id', 'email', 'name', 'description', 'phone',
                     'owner__first_name', 'owner__last_name', 'owner__email',]
    ordering = ['-id']

    def owner__first_name(self):
        return self.owner.first_name

    def owner__last_name(self):
        return self.owner.last_name

    def owner__email(self):
        return self.owner.email


@admin.register(FoodRecipe)
class FoodRecipeAdmin(admin.ModelAdmin):
    list_display = ['id',  'chef', 'name', 'category', 'is_active', 'date_joined',]
    list_filter = ['is_active', 'category',]
    search_fields = ['id', 'name', 'description',
                     'chef__name', 'chef__description', 'chef__email',]
    ordering = ['-id']

    def chef__name(self):
        return self.chef.name

    def chef__description(self):
        return self.chef.description

    def chef__email(self):
        return self.chef.email
