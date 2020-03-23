from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .helpers import get_address_by_cep
from .serializers import AddressSerializer


class AddressByCepView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AddressSerializer
    lookup_field = 'cep'

    def retrieve(self, request, *args, **kwargs):
        address = get_address_by_cep(self.kwargs.get(self.lookup_field))
        return Response(address, status=status.HTTP_200_OK)
