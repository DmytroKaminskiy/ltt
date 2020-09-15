from book.models import BookRent

from rest_framework import serializers


class BookRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRent
        fields = (
            'id',
            'price', 'price_period', 'days_period',
            'user_id', 'book', 'created', 'end',
            'status', 'days_period_initial',
        )

        extra_kwargs = {
            'price': {'read_only': True},
            'price_period': {'read_only': True},
            'days_period': {'read_only': True},
            'book': {'required': True},
            'created': {'read_only': True},
            'end': {'read_only': True},
            'days_period_initial': {'read_only': True},
        }
