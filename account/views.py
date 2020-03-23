from django.contrib.auth import get_user_model

from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.response import Response

from .serializers import SignUpSerializer, AccountInfoSerializer, AccountChangePasswordSerializer
from utils.helpers import separate_full_name


User = get_user_model()


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        phone = serializer.data.get('phone')
        address = serializer.data.get('address')
        email = serializer.data.get('email')
        password = request.data.get('password')

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            is_active=True,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountInfoView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountInfoSerializer

    def get_object(self):
        return self.request.user


class AccountChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountChangePasswordSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response({'success': True, 'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
