"""
URL configuration for creditcardactivity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('transaction/authorization', views.txn_authed, name='txn_authed'),
    path('transaction/settled', views.txn_settled, name='txn_settled'),
    path('transaction/authorization-cleared', views.txn_auth_cleared, name='txn_auth_cleared'),
    path('payment/initiated', views.pymt_initiated, name='pymt_initiated'),
    path('payment/posted', views.pymt_posted, name='pymt_posted'),
    path('payment/canceled', views.pymt_canceled, name='pymt_canceled'),
    path('users/<str:userId>/summary', views.user_summary, name='user_summary'),
    path('users/<str:userId>/detailed-summary', views.user_detailed_summary, name='user_summary'),
]
