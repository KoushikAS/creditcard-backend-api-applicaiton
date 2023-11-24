from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

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

def get_or_create_user(userId):
    try:
        user = User.objects.get(userId=userId)
    except User.DoesNotExist:
        user = User(userId=userId, balance=0, available_credit=INITIAL_CREDIT)
        user.save()
    return user

def validate_request_data(request_data):
    request_serializer = RequestSerializer(data=request_data)

    if not request_serializer.is_valid():
        return JsonResponse({'error': request_serializer.errors}, status=400)

    return None  # Validation successful

@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()}
)
@api_view(['POST'])
def txn_authed(request):
    request_data = request.data

    validation_error = validate_request_data(request_data)
    if validation_error:
        return validation_error

    # Extract data from the deserialized request
    userId = request_data['userId']
    txnId = request_data['txnId']
    timeStamp = request_data['timeStamp']
    amount = request_data['amount']

    if not Pending_Transaction.objects.filter(txnId=txnId, is_canceled = False).exists():

        user = get_or_create_user(userId)
        user.available_credit -= amount
        user.save()

        # Create a new pending transaction
        pending_transaction = Pending_Transaction(
            userId=user,
            txnId=txnId,
            amount=amount,
            initialTime=timeStamp,
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
    request_data = request.data

    validation_error = validate_request_data(request_data)
    if validation_error:
        return validation_error

    # Extract data from the deserialized request
    userId = request_data['userId']
    txnId = request_data['txnId']
    timeStamp = request_data['timeStamp']
    amount = request_data['amount']

    try:
        # Get the pending transaction based on txnId and userId
        pending_transaction = Pending_Transaction.objects.get(txnId=txnId, userId__userId=userId, is_settled = False, is_canceled = False )

        user = get_or_create_user(userId)

        user.available_credit += pending_transaction.amount
        user.available_credit -= amount
        user.balance += amount

        settled_transaction = Settled_Transaction(txnId = txnId, userId = user, amount = amount, eventTime = timeStamp, finalTime = timeStamp,initialTime = pending_transaction.initialTime)
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
    request_data = request.data

    validation_error = validate_request_data(request_data)
    if validation_error:
        return validation_error

    # Extract data from the deserialized request
    userId = request_data['userId']
    txnId = request_data['txnId']

    try:
        # Get the pending transaction based on txnId and userId
        pending_transaction = Pending_Transaction.objects.get(txnId=txnId, userId__userId=userId, is_settled = False, is_canceled = False)

        user = get_or_create_user(userId)

        user.available_credit += pending_transaction.amount
        pending_transaction.is_canceled = True
        user.save()
        pending_transaction.save()

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
    request_data = request.data

    validation_error = validate_request_data(request_data)
    if validation_error:
        return validation_error

    # Extract data from the deserialized request
    userId = request_data['userId']
    txnId = request_data['txnId']
    timeStamp = request_data['timeStamp']
    amount = int(request_data['amount'])

    if not Pending_Transaction.objects.filter(txnId=txnId, is_canceled = False).exists():
        user = get_or_create_user(userId)
        user.balance += amount
        user.save()

        # Create a new pending transaction
        pending_transaction = Pending_Transaction(
            userId=user,
            txnId=txnId,
            amount=amount,
            initialTime=timeStamp
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
    request_data = request.data

    validation_error = validate_request_data(request_data)
    if validation_error:
        return validation_error

    # Extract data from the deserialized request
    userId = request_data['userId']
    txnId = request_data['txnId']
    timeStamp = request_data['timeStamp']
    amount = request_data['amount']

    try:
        # Get the pending transaction based on txnId and userId
        pending_transaction = Pending_Transaction.objects.get(txnId=txnId, userId__userId=userId, is_settled = False, is_canceled = False)

        user = get_or_create_user(userId)

        user.available_credit -= pending_transaction.amount
        settled_transaction = Settled_Transaction(txnId = txnId, userId = user, amount = amount, finalTime = timeStamp,initialTime = pending_transaction.initialTime )
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
    request_data = request.data

    validation_error = validate_request_data(request_data)
    if validation_error:
        return validation_error

    # Extract data from the deserialized request
    userId = request_data['userId']
    txnId = request_data['txnId']

    try:
        # Get the pending transaction based on txnId and userId
        pending_transaction = Pending_Transaction.objects.get(txnId=txnId, userId__userId=userId, is_settled = False, is_canceled = False)

        user = get_or_create_user(userId)
        pending_transaction.is_canceled = True

        user.balance -= pending_transaction.amount
        user.save()
        pending_transaction.save()

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

@api_view(['GET'])
def user_summary(request, userId):
    try:
        # Retrieve the user data based on the userId
        user = User.objects.get(userId=userId)

        # Serialize the user data using the UserSummarySerializer
        serializer = UserQuickSummarySerializer(user)

        # Return the serialized user data as a JSON response
        return Response(serializer.data)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return Response({'error': 'User not found'}, status=404)

@api_view(['GET'])
def user_detailed_summary(request, userId):
    try:
        # Retrieve the user data based on the userId
        user = User.objects.get(userId=userId)
        pending_transactions = Pending_Transaction.objects.filter(userId__userId=userId, is_settled=False)
        settled_transactions = Settled_Transaction.objects.filter(userId__userId=userId)

        formatted_pending_transactions = []
        for transaction in pending_transactions.reverse():
            formatted_transaction = f"{transaction.txnId}: {transaction.amount} @ time {transaction.initialTime}"
            formatted_pending_transactions.append(formatted_transaction)

        formatted_settled_transactions = []
        for transaction in settled_transactions.reverse():
            formatted_transaction = f"{transaction.txnId}: {transaction.amount} @ time {transaction.initialTime} ( finalized @ time {transaction.finalTime} )"
            formatted_settled_transactions.append(formatted_transaction)

        # Serialize the user data using the UserSummarySerializer
        serializer = UserDetailedSummarySerializer(user)
        serializer.data['pending_transactions'] = formatted_pending_transactions
        serializer.data['settled_transactions'] = formatted_settled_transactions

        serializer = UserDetailedSummarySerializer({
            'userId': user.userId,
            'balance': user.balance,
            'available_credit': user.available_credit,
            'pending_transactions': formatted_pending_transactions,
            'settled_transactions': formatted_settled_transactions,
        })

        print(formatted_pending_transactions)
        # Return the serialized user data as a JSON response
        return Response(serializer.data)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return Response({'error': 'User not found'}, status=404)