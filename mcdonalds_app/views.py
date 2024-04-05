from django.http import Http404
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        try:
            return self.queryset.get(name=self.kwargs["product_name"])
        except Product.DoesNotExist:
            raise Http404


class ProductFieldDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        product_name = self.kwargs["product_name"]
        product_field = self.kwargs["product_field"]

        try:
            product = self.queryset.get(name=product_name)
            if hasattr(product, product_field):
                return {product_field: getattr(product, product_field)}
            else:
                raise Http404("Product field not found")
        except Product.DoesNotExist:
            raise Http404("Product not found")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(instance)

