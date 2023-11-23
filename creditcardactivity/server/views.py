from django.shortcuts import render
from django.http import HttpResponse

def txn_authed(request):
    print("Hello")
    return HttpResponse("This is a view for feature_one.")

