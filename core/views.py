
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from .permissions import IsAdminOrSuperAdmin, IsSuperAdmin
from django.contrib.auth.decorators import login_required, user_passes_test


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        task = self.get_object()
        if self.request.user != task.assigned_to:
            raise PermissionDenied("You are not allowed to update this task.")
        serializer.save()

class TaskReportView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request, id):
        try:
            task = Task.objects.get(id=id, status='Completed')
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found or not completed.'}, status=404)


# Admin Panel HTML Views
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.filter(assigned_admin=request.user)
    tasks = Task.objects.filter(assigned_to__in=users)
    return render(request, 'admin/dashboard.html', {
        'users': users,
        'tasks': tasks,
    })

@login_required
@user_passes_test(is_admin)
def task_reports(request):
    users = User.objects.filter(assigned_admin=request.user)
    tasks = Task.objects.filter(assigned_to__in=users, status='Completed')
    return render(request, 'admin/task_reports.html', {'tasks': tasks})
