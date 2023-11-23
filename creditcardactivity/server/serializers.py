from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    user_ID = serializers.CharField(max_length=100)
    txn_ID = serializers.CharField(max_length=100)
    timeStamp = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class ResponseSerializer(serializers.Serializer):
    RESPONSE_CHOICES = (
        ('SUCCESS', 'SUCCESS'),
        ('ERROR', 'ERROR'),
    )
    response = serializers.ChoiceField(choices=RESPONSE_CHOICES)
    description = serializers.CharField()