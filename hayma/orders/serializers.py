from rest_framework import serializers
from .models import Order, OrderItem
from catalog.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'shipping_address', 'payment_method', 'coupon', 'subtotal', 'discount', 'total', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'status', 'subtotal', 'discount', 'total', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context['request'].user
        order = Order.objects.create(user=user, status=Order.STATUS_PENDING, **validated_data)
        subtotal = 0
        for item in items_data:
            price = item.get('price')
            quantity = item.get('quantity', 1)
            subtotal += price * quantity
            OrderItem.objects.create(order=order, product_id=item['product_id'], quantity=quantity, price=price)
        order.subtotal = subtotal
        # Discount can be calculated via coupon in views; keep 0 by default
        order.total = subtotal - order.discount
        order.save()
        return order

