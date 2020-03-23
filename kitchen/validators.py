from rest_framework import exceptions

from .models import Chef


class ChefFieldValidator:
    def __init__(self, serializer):
        self.serializer = serializer

    def __call__(self, value):
        owner_id = self.serializer.get('request').user.id
        chef_ids = Chef.objects.filter(owner_id=owner_id, chef_id=value)
        if not chef_ids:
            raise exceptions.NotFound('Chef not found.')
