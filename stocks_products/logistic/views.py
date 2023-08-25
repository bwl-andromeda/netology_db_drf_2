from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django.db.models import Q

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductPagination(LimitOffsetPagination):
    default_limit = 10


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    pagination_class = ProductPagination


class StockFilter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(
                Q(products__title__icontains=search) |
                Q(products__description__icontains=search)
            )
        return queryset


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    filter_backends = [StockFilter]

    pagination_class = ProductPagination
