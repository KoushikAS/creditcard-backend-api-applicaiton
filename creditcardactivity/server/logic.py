from .helper_functions import *


def process_txn_authed(user, txnId, amount, initial_time):
    user.available_credit -= amount
    user.save()

    pending_transaction = Pending_Transaction(userId=user, txnId=txnId, amount=amount, initialTime=initial_time)
    pending_transaction.save()

    return JsonResponse({'response': 'SUCCESS', 'description': 'Successful Authorized Transaction'})


def process_pymt_initiated(user, txnId, amount, initial_time):
    user.balance += amount
    user.save()

    pending_transaction = Pending_Transaction(userId=user, txnId=txnId, amount=amount, initialTime=initial_time)
    pending_transaction.save()

    return JsonResponse({'response': 'SUCCESS', 'description': 'Successful Initiated Payment'})


def process_auth_cleared(user, txnId):
    pending_transaction = Pending_Transaction.objects.filter(userId=user, txnId=txnId, is_canceled=False,
                                                             is_settled=False).first()

    user.available_credit += pending_transaction.amount
    user.save()
    pending_transaction.is_canceled = True
    pending_transaction.save()

    return JsonResponse({'response': 'SUCCESS', 'description': 'Successful Cleared Auth'})


def process_pymt_canceled(user, txnId):
    pending_transaction = Pending_Transaction.objects.filter(userId=user, txnId=txnId, is_canceled=False,
                                                             is_settled=False).first()

    user.balance -= pending_transaction.amount
    user.save()
    pending_transaction.is_canceled = True
    pending_transaction.save()

    return JsonResponse({'response': 'SUCCESS', 'description': 'Successful Canceled Payment'})


def process_txn_settled(user, txnId, amount, final_time):
    pending_transaction = Pending_Transaction.objects.filter(userId=user, txnId=txnId, is_canceled=False,
                                                             is_settled=False).first()

    user.available_credit += pending_transaction.amount
    user.available_credit -= amount
    user.balance += amount

    settled_transaction = Settled_Transaction(txnId=txnId, userId=user, amount=amount,
                                              finalTime=final_time, initialTime=pending_transaction.initialTime)
    pending_transaction.is_settled = True

    settled_transaction.save()
    user.save()
    pending_transaction.save()

    return JsonResponse({'response': 'SUCCESS', 'description': 'Successful Settled Transaction'})


def process_pymt_posted(user, txnId, final_time):
    pending_transaction = Pending_Transaction.objects.filter(userId=user, txnId=txnId, is_canceled=False,
                                                             is_settled=False).first()

    user.available_credit -= pending_transaction.amount

    settled_transaction = Settled_Transaction(txnId=txnId, userId=user, amount=pending_transaction.amount,
                                              finalTime=final_time, initialTime=pending_transaction.initialTime)
    pending_transaction.is_settled = True

    settled_transaction.save()
    user.save()
    pending_transaction.save()

    return JsonResponse({'response': 'SUCCESS', 'description': 'Successful Posted Payment'})
