from decimal import Decimal

from django.http import JsonResponse

from .models import *
from .serializers import *

INITIAL_CREDIT = 1000


def sendResponse(data):
    response = ResponseSerializer(data=data)

    if not response.is_valid():
        return JsonResponse({'error': response.errors}, status=400)

    return JsonResponse(response.data)


def get_or_create_user(user_id):
    user, created = User.objects.get_or_create(userId=user_id,
                                               defaults={'balance': 0, 'available_credit': INITIAL_CREDIT})
    return user


def validate_request_data(request_data):
    request_serializer = RequestSerializer(data=request_data)

    if not request_serializer.is_valid():
        return JsonResponse({'error': request_serializer.errors}, status=400)

    return None  # Validation successful


def handle_transaction_error():
    return JsonResponse({'response': 'ERROR', 'description': 'Transaction Id is not present in pending transaction'})



def extract_request_data(request_data):
    user_id = request_data['userId']
    txn_id = request_data['txnId']
    timeStamp = request_data['timeStamp']
    amount = Decimal(request_data['amount'])
    return user_id, txn_id, timeStamp, amount
