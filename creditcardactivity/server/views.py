from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .logic import *


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()},
    operation_description="This endpoint authorizes transactions. It requires userId, txnId, timestamp, and amount. Non-existent userIds trigger the creation of a new user with 1000 credits."
)
@api_view(['POST'])
def txn_authed(request):
    request_data = request.data
    validation_error = validate_request_data(request_data)

    if validation_error:
        return validation_error

    userId, txnId, timeStamp, amount = extract_request_data(request_data)

    if not Pending_Transaction.objects.filter(txnId=txnId).exists():
        user = get_or_create_user(userId)
        return process_txn_authed(user, txnId, amount, timeStamp)
    else:
        return JsonResponse({'response': 'ERROR', 'description': 'Transaction Id already Exists'})


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()},
    operation_description="This endpoint is to a previously authorized transaction settling. Txn settlement events specify the same txn id as the corresponding auth event, but they have their own timestamp, and the amount can change."
)
@api_view(['POST'])
def txn_settled(request):
    request_data = request.data
    validation_error = validate_request_data(request_data)

    if validation_error:
        return validation_error

    userId, txnId, timeStamp, amount = extract_request_data(request_data)

    if Pending_Transaction.objects.filter(txnId=txnId, userId=userId, is_canceled=False, is_settled=False).exists():
        user = get_or_create_user(userId)
        return process_txn_settled(user, txnId, amount, timeStamp)
    else:
        return JsonResponse({'response': 'ERROR', 'description': 'Transaction Id does not Exists'})


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()},
    operation_description="This endpoint is to a previously authorized transaction being cleared. Txn cleared events specify the same txnId as the corresponding auth event, too. (Amount and timestamp field will be ignored as it is not required.) "
)
@api_view(['POST'])
def txn_auth_cleared(request):
    request_data = request.data
    validation_error = validate_request_data(request_data)

    if validation_error:
        return validation_error

    userId, txnId, _, _ = extract_request_data(request_data)

    if Pending_Transaction.objects.filter(txnId=txnId, is_canceled=False, is_settled=False).exists():
        user = get_or_create_user(userId)
        return process_auth_cleared(user, txnId)
    else:
        return JsonResponse({'response': 'ERROR', 'description': 'Transaction Id does not Exists'})


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()},
    operation_description="This endpoint is to a payment being initiated. These events are similar to txn auth events. Enter the Payment amount in postive, I have taken care to make it negative in backend since they lower the balance."
)
@api_view(['POST'])
def pymt_initiated(request):
    request_data = request.data
    validation_error = validate_request_data(request_data)

    if validation_error:
        return validation_error

    userId, txnId, timeStamp, amount = extract_request_data(request_data)

    if not Pending_Transaction.objects.filter(txnId=txnId).exists():
        user = get_or_create_user(userId)
        return process_pymt_initiated(user, txnId, -amount, timeStamp)
    else:
        return JsonResponse({'response': 'ERROR', 'description': 'Transaction Id already Exists'})


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()},
    operation_description="This endpoint is to these correspond to a payment posting. These events are similar to txn settled events. (Since payment amounts can't and don't change. Therefore Amount and timestamp field will be ignored)."
)
@api_view(['POST'])
def pymt_posted(request):
    request_data = request.data
    validation_error = validate_request_data(request_data)

    if validation_error:
        return validation_error

    userId, txnId, timeStamp, amount = extract_request_data(request_data)

    if Pending_Transaction.objects.filter(txnId=txnId, userId=userId, is_canceled=False, is_settled=False).exists():
        user = get_or_create_user(userId)
        return process_pymt_posted(user, txnId, timeStamp)
    else:
        return JsonResponse({'response': 'ERROR', 'description': 'Transaction Id does not Exists'})


@swagger_auto_schema(
    method='post',
    request_body=RequestSerializer,
    responses={200: ResponseSerializer()},
    operation_description="This endpoint is to these correspond to a payment getting canceled. These events are similar to txn cleared events."
)
@api_view(['POST'])
def pymt_canceled(request):
    request_data = request.data
    validation_error = validate_request_data(request_data)

    if validation_error:
        return validation_error

    userId, txnId, _, _ = extract_request_data(request_data)

    if Pending_Transaction.objects.filter(txnId=txnId, is_canceled=False, is_settled=False).exists():
        user = get_or_create_user(userId)
        return process_pymt_canceled(user, txnId)
    else:
        return JsonResponse({'response': 'ERROR', 'description': 'Transaction Id does not Exists'})


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
            if transaction.is_canceled:
                formatted_transaction = f"{transaction.txnId}: {transaction.amount} @ time {transaction.initialTime} (Canceled)"
            else:
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

        # Return the serialized user data as a JSON response
        return Response(serializer.data)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return Response({'error': 'User not found'}, status=404)
