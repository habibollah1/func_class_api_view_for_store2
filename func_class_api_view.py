from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.views import APIView

from .models import Product, Category
from .serializers import ProductSerializers, CategorySerializers

################################### مرحله سوم

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializers

    def get_serializer_context(self):  # صرفا در مواقع استفاده از hyperlink
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializers

    def delete(self, request, *args, **kwargs):
        product = Product.objects.select_related('category')
        if product.order_items.count() > 0:
            return Response({'error': 'there is some order items including this product. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializers


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.prefetch_related('products')
    serializer_class = CategorySerializers

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'there is some products including this category. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response()


#################################### مرحله اول و دوم


class ProductList(APIView):
    def get(self, request):
        products_queryset = Product.objects.select_related('category').all()
        serializer = ProductSerializers(products_queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products_queryset = Product.objects.select_related('category').all()
#         serializer = ProductSerializers(products_queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        serializer = ProductSerializers(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        serializer = ProductSerializers(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'there is some order items including this product. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE', ])
# def product_detail(request, pk):
#     product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#
#     if request.method == 'GET':
#         serializer = ProductSerializers(product, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializers(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.order_items.count() > 0:
#             return Response({'error': 'there is some order items including this product. please remove them first'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# if serializer.is_valid():
# else:
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# return Response('all ok')

class CategoryList(APIView):
    def get(self, request):
        category_queryset = Category.objects.prefetch_related('products').all()
        serializer = CategorySerializers(category_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'POST'])
# def category_list(request):
#     if request.method == 'GET':
#         # category_queryset = Category.objects.prefetch_related('products').all()
#         category_queryset = Category.objects.annotate(
#             products_count=Count('products')
#         ).all()
#         serializer = CategorySerializers(category_queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # category_queryset = Category.objects.prefetch_related('products').all()
#         serializer = CategorySerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


# .objects.prefetch_related('category')

class CategoryDetail(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if request.method == 'GET':
            serializer = CategorySerializers(category)
            return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializers(category.objects.prefetch_related('products'), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'there is some products including this category. please remove them first'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response()


# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     if request.method == 'GET':
#         serializer = CategorySerializers(category)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = CategorySerializers(category.objects.annotate(products_count=Count('products')), data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if category.products.count() > 0:
#             return Response({'error': 'there is some products including this category. please remove them first'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response()

# product = get_object_or_404(Product, pk=id)
# try: # نتیجه این 4 خط همون بالایی هس
#     product = Product.objects.get(pk=
# except Product.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)
