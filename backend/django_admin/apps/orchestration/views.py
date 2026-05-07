from __future__ import annotations

import os

from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import FastAPIOrchestrator


class PlatformOverviewView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orchestrator = FastAPIOrchestrator(os.getenv('FASTAPI_BASE_URL', 'http://fastapi:8000/api/v1'))
        health = async_to_sync(orchestrator.fetch_health)()
        metrics = async_to_sync(orchestrator.fetch_metrics)()
        return Response({'fastapi': health, 'metrics': metrics})


class QueueStatusView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({'celery': 'healthy', 'redis': 'healthy', 'audit_logs': 'enabled'})
