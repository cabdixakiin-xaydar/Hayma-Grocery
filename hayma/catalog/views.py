from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product, Coupon
from .serializers import CategorySerializer, ProductSerializer, CouponSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @property
    def admin_queryset(self):
        return Product.objects.all().order_by('-created_at')

    def get_queryset(self):
        if self.request and self.request.user and self.request.user.is_staff:
            return self.admin_queryset
        return super().get_queryset()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def low_stock(self, request):
        try:
            threshold = int(request.query_params.get('threshold', '5'))
        except ValueError:
            threshold = 5
        qs = self.admin_queryset.filter(stock__lte=threshold)
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def wishlist(self, request, pk=None):
        product = self.get_object()
        product.wishlist_users.add(request.user)
        return Response({'detail': 'Added to wishlist'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unwishlist(self, request, pk=None):
        product = self.get_object()
        product.wishlist_users.remove(request.user)
        return Response({'detail': 'Removed from wishlist'})


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]

# Create your views here.
