import decimal

from django.utils import timezone
from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    userId = serializers.CharField(max_length=100)
    txnId = serializers.CharField(max_length=100)
    timeStamp = serializers.CharField(required=False, default=timezone.now().strftime('%Y-%m-%d %H:%M:%S'))
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=decimal.Decimal('0.00'))

class ResponseSerializer(serializers.Serializer):
    RESPONSE_CHOICES = (
        ('SUCCESS', 'SUCCESS'),
        ('ERROR', 'ERROR'),
    )
    response = serializers.ChoiceField(choices=RESPONSE_CHOICES)
    description = serializers.CharField()

class UserQuickSummarySerializer(serializers.Serializer):
    userId = serializers.CharField(max_length=100)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    available_credit = serializers.DecimalField(max_digits=10, decimal_places=2)

class UserDetailedSummarySerializer(serializers.Serializer):
    userId = serializers.CharField(max_length=100)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    available_credit = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_transactions = serializers.ListField(child=serializers.CharField(max_length=50),allow_empty=True,required=False)
    settled_transactions = serializers.ListField(child=serializers.CharField(max_length=50),allow_empty=True,required=False)
