from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DailyLog
from .serializers import DailyLogSerializer

class DailyLogViewSet(viewsets.ModelViewSet):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent logs for dashboard"""
        recent_logs = DailyLog.objects.select_related('user').order_by('-date')[:5]
        serializer = self.get_serializer(recent_logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_logs(self, request):
        """Get current user's logs"""
        user_logs = DailyLog.objects.filter(user=request.user).order_by('-date')
        serializer = self.get_serializer(user_logs, many=True)
        return Response(serializer.data)