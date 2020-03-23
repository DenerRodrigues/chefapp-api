from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Chef, FoodRecipe
from .serializers import ChefCreateListSerializer, ChefRetrieveUpdateDestroySerializer
from .serializers import FoodRecipeListCreateSerializer, FoodRecipeRetrieveUpdateDestroySerializer


User = get_user_model()


class ChefListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChefCreateListSerializer

    def get_queryset(self):
        return Chef.objects.filter(is_active=True, owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.instance = Chef.objects.create(
            owner=self.request.user,
            name=serializer.data.get('name'),
            description=serializer.data.get('description', ''),
            email=serializer.data.get('email'),
            phone=serializer.data.get('phone'),
            address=serializer.data.get('address'),
            open_at=serializer.data.get('open_at'),
            close_at=serializer.data.get('close_at'),
            days_of_weak=serializer.data.get('days_of_weak'),
        )
        return serializer.instance
    

class ChefRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChefRetrieveUpdateDestroySerializer
    lookup_field = 'id'

    def get_object(self):
        return get_object_or_404(Chef, id=self.kwargs.get(self.lookup_field), owner=self.request.user)


class ChefPublicListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChefCreateListSerializer

    def get_queryset(self):
        return Chef.objects.filter(is_active=True)


class FoodRecipeListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FoodRecipeListCreateSerializer
    lookup_field = 'chef_id'

    def get_queryset(self):
        return FoodRecipe.objects.filter(
            is_active=True,
            chef_id=self.kwargs.get(self.lookup_field),
            chef__owner=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.instance = FoodRecipe.objects.create(
            chef_id=self.kwargs.get(self.lookup_field),
            name=serializer.data.get('name'),
            description=serializer.data.get('description', ''),
            category=serializer.data.get('category'),
            price=serializer.data.get('price'),
            preparation_time=serializer.data.get('preparation_time'),
        )
        return serializer.instance


class FoodRecipeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FoodRecipeRetrieveUpdateDestroySerializer
    lookup_field = 'id'

    def get_object(self):
        return get_object_or_404(
            FoodRecipe,
            id=self.kwargs.get(self.lookup_field),
            chef__owner=self.request.user,
            is_active=True,
        )


class FoodRecipePublicListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FoodRecipeListCreateSerializer

    def get_queryset(self):
        query_filter = {
            'is_active': True
        }
        filters = self.request.query_params
        if filters.get('chef_id'):
            query_filter['chef_id__in'] = filters.get('chef_id').split(',')
        if filters.get('category'):
            query_filter['category__in'] = filters.get('category').split(',')
        
        return FoodRecipe.objects.filter(**query_filter)


class FoodRecipeCategoryListView(ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(dict(FoodRecipe.CATEGORY_CHOICES).keys(), status=status.HTTP_200_OK)
