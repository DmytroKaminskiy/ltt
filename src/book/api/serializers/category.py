from book.models import Category

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name',
            'price', 'price_period', 'days_period',
        )

        extra_kwargs = {
            'price': {'required': True},
        }
