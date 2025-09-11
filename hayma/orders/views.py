from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from cart.models import CartItem, Cart
from catalog.models import Coupon, Product


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        request = self.request
        user = request.user
        data = request.data
        items_data = data.get('items') or []
        shipping_address = data.get('shipping_address')
        payment_method = data.get('payment_method', 'cod')

        # If no items provided, use cart items
        if not items_data:
            cart, _ = Cart.objects.get_or_create(user=user)
            cart_items = list(CartItem.objects.filter(cart=cart).select_related('product'))
            if not cart_items:
                raise ValueError('Cart is empty')
            items_data = [
                {
                    'product_id': ci.product_id,
                    'quantity': ci.quantity,
                    'price': ci.product.price,
                }
                for ci in cart_items
            ]

        # Create order via serializer
        order = serializer.save(shipping_address=shipping_address, payment_method=payment_method)

        # Apply coupon by code if present
        coupon_code = data.get('coupon')
        subtotal = 0
        for item in items_data:
            product = Product.objects.select_for_update().get(pk=item['product_id'])
            quantity = item.get('quantity', 1)
            price = item.get('price')
            subtotal += price * quantity
        discount = 0
        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code, active=True).first()
            if coupon:
                order.coupon = coupon
                discount = subtotal * (coupon.discount_percent / 100)
        order.subtotal = subtotal
        order.discount = discount
        order.total = max(subtotal - discount, 0)
        order.save()

        # Create items and decrement stock
        for item in items_data:
            product = Product.objects.select_for_update().get(pk=item['product_id'])
            quantity = item.get('quantity', 1)
            price = item.get('price')
            from .models import OrderItem
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()

        # Clear cart
        CartItem.objects.filter(cart__user=user).delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def set_status(self, request, pk=None):
        order = self.get_object()
        status_value = request.data.get('status')
        valid_status = [s for s, _ in order.STATUS_CHOICES]
        if status_value not in valid_status:
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status_value
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if order.status != order.STATUS_PENDING:
            return Response({'detail': 'Cannot cancel'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = order.STATUS_CANCELLED
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def analytics(self, request):
        qs = self.get_queryset()
        total_orders = qs.count()
        revenue = sum(o.total for o in qs)
        top_products = {}
        from .models import OrderItem
        for oi in OrderItem.objects.filter(order__in=qs).select_related('product'):
            top_products[oi.product.name] = top_products.get(oi.product.name, 0) + oi.quantity
        top = sorted(top_products.items(), key=lambda x: x[1], reverse=True)[:5]
        return Response({
            'total_orders': total_orders,
            'revenue': revenue,
            'top_products': top,
        })

# Create your views here.
