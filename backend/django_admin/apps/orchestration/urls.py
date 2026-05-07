from __future__ import annotations

from django.urls import path

from .views import PlatformOverviewView, QueueStatusView

urlpatterns = [
    path('overview/', PlatformOverviewView.as_view(), name='overview'),
    path('queue-status/', QueueStatusView.as_view(), name='queue-status'),
]
