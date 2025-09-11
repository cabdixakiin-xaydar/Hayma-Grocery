from rest_framework import views, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)


class CartItemView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=serializer.validated_data['product_id'],
            defaults={'quantity': serializer.validated_data.get('quantity', 1)},
        )
        if not created:
            item.quantity += serializer.validated_data.get('quantity', 1)
            item.save()
        return Response(CartSerializer(cart).data)

    def put(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            item = CartItem.objects.get(cart=cart, product_id=serializer.validated_data['product_id'])
            item.quantity = serializer.validated_data.get('quantity', item.quantity)
            item.save()
        except CartItem.DoesNotExist:
            return Response({'detail': 'Item not in cart'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CartSerializer(cart).data)

    def delete(self, request):
        cart = get_or_create_cart(request.user)
        product_id = request.data.get('product_id')
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response(CartSerializer(cart).data)

# Create your views here.
