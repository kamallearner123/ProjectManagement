from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get task statistics"""
        total = Task.objects.count()
        completed = Task.objects.filter(status='done').count()
        inprogress = Task.objects.filter(status='inprogress').count()
        todo = Task.objects.filter(status='todo').count()
        
        return Response({
            'total': total,
            'completed': completed,
            'inprogress': inprogress,
            'todo': todo
        })

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update task status"""
        task = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in ['todo', 'inprogress', 'done']:
            task.status = new_status
            task.save()
            return Response({'success': True, 'status': task.status})
        
        return Response({'success': False, 'error': 'Invalid status'}, 
                       status=status.HTTP_400_BAD_REQUEST)