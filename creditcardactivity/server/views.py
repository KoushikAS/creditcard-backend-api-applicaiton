from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from .models import *

INITIAL_CREDIT = 1000


# Helper functions

def sendResponse(data):
    # Serialize the response data using ResponseSerializer
    response = ResponseSerializer(data=data)

    if not response.is_valid():
        errors = response.errors
        return JsonResponse({'error': errors}, status=400)

    serialized_data = response.data
    return JsonResponse(serialized_data)

def get_or_create_user(user_id):
    try:
        user = User.objects.get(userId=user_id)
    except User.DoesNotExist:
        user = User(userId=user_id, balance=0, available_credit=INITIAL_CREDIT)
        user.save()
    return user

def is_transaction_id_exist(txn_id, model_class):
    return model_class.objects.filter(txnId=txn_id).exists()

@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()}
)
@api_view(['POST'])
def txn_authed(request):
    # Deserialize the request data using RequestSerializer
    request_serializer = RequestSerializer(data=request.data)

    if not request_serializer.is_valid():
        errors = request_serializer.errors
        return JsonResponse({'error': errors}, status=400)

    # Extract data from the deserialized request
    user_id = request_serializer.validated_data['user_ID']
    txn_id = request_serializer.validated_data['txn_ID']
    timeStamp = request_serializer.validated_data['timeStamp']
    amount = request_serializer.validated_data['amount']

    if not is_transaction_id_exist(txn_id, Pending_Transaction):

        user = get_or_create_user(user_id)
        user.available_credit -= amount
        user.save()

        # Create a new pending transaction
        pending_transaction = Pending_Transaction(
            userId=user,
            txnId=txn_id,
            amount=amount,
            eventTime=timeStamp,
            is_settled=False
        )
        pending_transaction.save()

        # Prepare the response data
        response = {
            'response': 'SUCCESS',
            'description': 'Successful Authorized Transaction'
        }
    else:
        # Prepare the response data
        response = {
            'response': 'ERROR',
            'description': 'Transaction Id already Exists'
        }

    return sendResponse(response)


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()}
)
@api_view(['POST'])
def txn_settled(request):
    # Deserialize the request data using RequestSerializer
    request_serializer = RequestSerializer(data=request.data)

    if not request_serializer.is_valid():
        errors = request_serializer.errors
        return JsonResponse({'error': errors}, status=400)

    # Extract data from the deserialized request
    user_id = request_serializer.validated_data['user_ID']
    txn_id = request_serializer.validated_data['txn_ID']
    timeStamp = request_serializer.validated_data['timeStamp']
    amount = request_serializer.validated_data['amount']

    try:
        # Get the pending transaction based on txn_id and user_id
        pending_transaction = Pending_Transaction.objects.get(txnId=txn_id, userId__userId=user_id, is_settled = False)

        user = get_or_create_user(user_id)

        user.available_credit += pending_transaction.amount
        user.available_credit -= amount
        user.balance += amount

        settled_transaction = Settled_Transaction(txnId = txn_id, userId = user, amount = amount, eventTime = timeStamp)
        pending_transaction.is_settled = True

        settled_transaction.save()
        user.save()
        pending_transaction.save()

        response = {
            'response': 'SUCCESS',
            'description': 'Successful Authorized Transaction'
        }

    except Pending_Transaction.DoesNotExist:
        response = {
            'response': 'ERROR',
            'description': 'Transaction Id is not present in pending transaction'
        }

    return sendResponse(response)


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()}
)
@api_view(['POST'])
def txn_auth_cleared(request):
    # Deserialize the request data using RequestSerializer
    request_serializer = RequestSerializer(data=request.data)

    if not request_serializer.is_valid():
        errors = request_serializer.errors
        return JsonResponse({'error': errors}, status=400)

    # Extract data from the deserialized request
    user_id = request_serializer.validated_data['user_ID']
    txn_id = request_serializer.validated_data['txn_ID']

    try:
        # Get the pending transaction based on txn_id and user_id
        pending_transaction = Pending_Transaction.objects.get(txnId=txn_id, userId__userId=user_id, is_settled = False)

        user = get_or_create_user(user_id)

        user.available_credit += pending_transaction.amount
        user.save()
        pending_transaction.delete()

        response = {
            'response': 'SUCCESS',
            'description': 'Successful Cleared Auth Transaction'
        }

    except Pending_Transaction.DoesNotExist:
        response = {
            'response': 'ERROR',
            'description': 'Transaction Id is not present in pending transaction'
        }

    return sendResponse(response)

@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()}
)
@api_view(['POST'])
def pymt_initiated(request):
    # Deserialize the request data using RequestSerializer
    request_serializer = RequestSerializer(data=request.data)

    if not request_serializer.is_valid():
        errors = request_serializer.errors
        return JsonResponse({'error': errors}, status=400)

    # Extract data from the deserialized request
    user_id = request_serializer.validated_data['user_ID']
    txn_id = request_serializer.validated_data['txn_ID']
    timeStamp = request_serializer.validated_data['timeStamp']
    amount = request_serializer.validated_data['amount']

    if not is_transaction_id_exist(txn_id, Pending_Transaction):
        user = get_or_create_user(user_id)
        user.balance += amount
        user.save()

        # Create a new pending transaction
        pending_transaction = Pending_Transaction(
            userId=user,
            txnId=txn_id,
            amount=amount,
            eventTime=timeStamp,
            is_settled=False
        )
        pending_transaction.save()

        # Prepare the response data
        response = {
            'response': 'SUCCESS',
            'description': 'Successful Initiated Payment'
        }
    else:
        # Prepare the response data
        response = {
            'response': 'ERROR',
            'description': 'Transaction Id already Exists'
        }

    return sendResponse(response)


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()}
)
@api_view(['POST'])
def pymt_posted(request):
    # Deserialize the request data using RequestSerializer
    request_serializer = RequestSerializer(data=request.data)

    if not request_serializer.is_valid():
        errors = request_serializer.errors
        return JsonResponse({'error': errors}, status=400)

    # Extract data from the deserialized request
    user_id = request_serializer.validated_data['user_ID']
    txn_id = request_serializer.validated_data['txn_ID']
    timeStamp = request_serializer.validated_data['timeStamp']
    amount = request_serializer.validated_data['amount']

    try:
        # Get the pending transaction based on txn_id and user_id
        pending_transaction = Pending_Transaction.objects.get(txnId=txn_id, userId__userId=user_id, is_settled = False)

        user = get_or_create_user(user_id)

        user.available_credit -= pending_transaction.amount
        settled_transaction = Settled_Transaction(txnId = txn_id, userId = user, amount = amount, eventTime = timeStamp)
        pending_transaction.is_settled = True

        settled_transaction.save()
        user.save()
        pending_transaction.save()

        response = {
            'response': 'SUCCESS',
            'description': 'Successful Posted Payment'
        }

    except Pending_Transaction.DoesNotExist:
        response = {
            'response': 'ERROR',
            'description': 'Transaction Id is not present in pending transaction'
        }

    return sendResponse(response)


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()}
)
@api_view(['POST'])
def pymt_canceled(request):
    # Deserialize the request data using RequestSerializer
    request_serializer = RequestSerializer(data=request.data)

    if not request_serializer.is_valid():
        errors = request_serializer.errors
        return JsonResponse({'error': errors}, status=400)

    # Extract data from the deserialized request
    user_id = request_serializer.validated_data['user_ID']
    txn_id = request_serializer.validated_data['txn_ID']

    try:
        # Get the pending transaction based on txn_id and user_id
        pending_transaction = Pending_Transaction.objects.get(txnId=txn_id, userId__userId=user_id, is_settled = False)

        user = get_or_create_user(user_id)

        user.balance -= pending_transaction.amount
        user.save()
        pending_transaction.delete()

        response = {
            'response': 'SUCCESS',
            'description': 'Successful Canceled Payment'
        }

    except Pending_Transaction.DoesNotExist:
        response = {
            'response': 'ERROR',
            'description': 'Transaction Id is not present in pending transaction'
        }

    return sendResponse(response)