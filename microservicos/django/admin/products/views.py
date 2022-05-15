

from products.models import Product, User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from products.serializers import ProductSerializer
from .producer import publish
import random


class ProductViewSet(viewsets.ModelViewSet):
    # List all products
    def list(self, request):
        # /api/products
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new product
    def create(self, request):
        # /api/products
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_create',serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Retrieve one product with id
    def retrieve(self, request, pk=None):
        # /api/products/<str:id>
        #product = Product.objects.get(pk=pk)
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update one product with id
    def update(self, request, pk=None):
        # /api/products/<str:id>

        #product = Product.objects.get(pk=pk)
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated',serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # Delete one product with id

    def destroy(self, request, pk=None):
        # /api/products/<str:id>
        #product = Product.objects.get(pk=pk)
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        publish('product_deleted',pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        #users = get_object_or_404(User)
        user = random.choice(users)
        return Response({
            'id': user.id,
        })
