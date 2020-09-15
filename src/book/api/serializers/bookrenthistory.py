from book.models import RentDayHistory

from rest_framework import serializers


class RentDayHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RentDayHistory
        fields = (
            'id', 'rent_id', 'amount', 'created',
        )

        extra_kwargs = {
            'rent_id': {'read_only': True},
            'amount': {'read_only': True},
            'created': {'read_only': True},
        }
