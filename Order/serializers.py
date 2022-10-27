from rest_framework import serializers
from Order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'driver',
            'order_datetime',
            'description',
            'lat_pickup',
            'lng_pickup',
            'lat_deliver',
            'lng_deliver'
        )

        model = Order


