from django.urls import path
from .views import *


urlpatterns = [
    path('packages/', PackageView.as_view()),
    path('subscriptions/', SubscriptionView.as_view()),
]
