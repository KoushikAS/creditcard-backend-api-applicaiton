
import math
import os
import random
import re
import sys

#
# Complete the 'summarize' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING inputJSON as parameter.
#
import json


def summarize(inputJSON):
    # Write your code here

    data = json.loads(inputJSON)

    events = data['events']
    credit_limit = data['creditLimit']

    available_credit = credit_limit
    payable_balance = 0
    pending_transactions = []
    settled_transactions = []

    for event in events:
        event_type = event['eventType']

        if event_type == 'TXN_AUTHED':
            amount = event['amount']
            available_credit -= amount
            # TODO for safety check what if the transction id already exists?
            pending_transactions.append((event['txnId'], amount, event['eventTime']))

        elif event_type == 'TXN_SETTLED':

            txn_id = event['txnId']
            amount = event['amount']

            for i, (pending_txn_id, pending_amount, pending_event_time) in enumerate(pending_transactions):
                # TODO: for safety check what happens if it does not find the transactionId
                if pending_txn_id == txn_id:
                    available_credit += pending_amount
                    available_credit -= amount
                    payable_balance += amount
                    pending_transactions.pop(i)
                    settled_transactions.append((txn_id, amount, pending_event_time, event['eventTime']))
                    break


        elif event_type == 'TXN_AUTH_CLEARED':
            txn_id = event['txnId']
            for i, (pending_txn_id, pending_amount, _) in enumerate(pending_transactions):
                # TODO: for safety check what happens if it does not find the transactionId
                if pending_txn_id == txn_id:
                    available_credit += pending_amount
                    pending_transactions.pop(i)
                    break

        elif event_type == 'PAYMENT_INITIATED':
            amount = event['amount']
            payable_balance += amount

            pending_transactions.append((event['txnId'], amount, event['eventTime']))

        elif event_type == 'PAYMENT_POSTED':
            txn_id = event['txnId']
            for i, (pending_txn_id, pending_amount, pending_event_time) in enumerate(pending_transactions):
                if pending_txn_id == txn_id:
                    available_credit -= pending_amount
                    pending_transactions.pop(i)
                    settled_transactions.append((txn_id, pending_amount, pending_event_time, event['eventTime']))
                    break

        elif event_type == 'PAYMENT_CANCELED':
            txn_id = event['txnId']
            for i, (pending_txn_id, pending_amount, _) in enumerate(pending_transactions):
                if pending_txn_id == txn_id:
                    payable_balance -= pending_amount
                    pending_transactions.pop(i)
                    break

    pending_transactions.sort(key=lambda x: x[2], reverse=True)
    settled_transactions.sort(key=lambda x: x[2], reverse=True)

    summary_lines = [
        f"Available credit: {'-' if available_credit < 0 else ''}${abs(available_credit)}",
        f"Payable balance: {'-' if payable_balance < 0 else ''}${abs(payable_balance)}",
        f"\nPending transactions:",
        *[f"{txn_id}: {'-' if amount < 0 else ''}${abs(amount)} @ time {event_time}" for txn_id, amount, event_time in
          pending_transactions],
        f"\nSettled transactions:",
        *[
            f"{txn_id}: {'-' if amount < 0 else ''}${abs(amount)} @ time {pending_event_time} (finalized @ time {settled_event_time})"
            for txn_id, amount, pending_event_time, settled_event_time in settled_transactions],
    ]

    summary_str = "\n".join(summary_lines).strip()

    return summary_str


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    inputJSON = input()

    result = summarize(inputJSON)

    fptr.write(result + '\n')

    fptr.close()
