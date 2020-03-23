from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    cep = serializers.CharField(required=True)
    street = serializers.CharField(required=True)
    number = serializers.CharField(required=True)
    complement = serializers.CharField(required=False)
    neighborhood = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
