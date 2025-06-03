
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task, User
from .serializers import TaskSerializer, TaskUpdateSerializer
from .permissions import IsAdminOrSuperAdmin, IsSuperAdmin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .forms import TaskForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import UserForm
from django.http import HttpResponse


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
def role_based_redirect(request):
    user = request.user
    print(f"User role: {user.role} {user}")  # Debugging line to check user role
    if user.role == 'superadmin':
        return redirect('superadmin-dashboard')
    elif user.role == 'admin':
        return redirect('admin-dashboard')
    else:
        return HttpResponse("Unauthorized: You do not have access to a dashboard.", status=403)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    print(f"User role: {request.user.role} {request.user}")  # Debugging line to check user role
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

@login_required
@user_passes_test(is_admin)
def assign_task(request):
    users = User.objects.filter(assigned_admin=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if task.assigned_to in users:
                task.save()
                messages.success(request, "Task assigned successfully.")
                return redirect('admin-dashboard')
            else:
                messages.error(request, "You can only assign tasks to your users.")
    else:
        form = TaskForm()
        form.fields['assigned_to'].queryset = users
    return render(request, 'admin/assign_task.html', {'form': form})




def is_superadmin(user):
    return user.is_authenticated and user.role == 'superadmin'

@login_required
@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    users = User.objects.all()
    tasks = Task.objects.all()
    return render(request, 'superadmin/dashboard.html', {
        'users': users,
        'tasks': tasks,
    })

@login_required
@user_passes_test(is_superadmin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'superadmin/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_superadmin)
def manage_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'superadmin/manage_tasks.html', {'tasks': tasks})

######Manage Users Views######

@login_required
@user_passes_test(is_superadmin)
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('manage-users')
    else:
        form = UserForm()
    return render(request, 'superadmin/create_user.html', {'form': form})

@login_required
@user_passes_test(is_superadmin)
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('manage-users')
    else:
        form = UserForm(instance=user)
    return render(request, 'superadmin/edit_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_superadmin)
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('manage-users')
    return render(request, 'superadmin/delete_user.html', {'user': user})

## Manage Tasks Views

@login_required
@user_passes_test(is_superadmin)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully.")
            return redirect('manage-tasks')
    else:
        form = TaskForm()
    return render(request, 'superadmin/create_task.html', {'form': form})

@login_required
@user_passes_test(is_superadmin)
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('manage-tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'superadmin/edit_task.html', {'form': form, 'task': task})

@login_required
@user_passes_test(is_superadmin)
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('manage-tasks')
    return render(request, 'superadmin/delete_task.html', {'task': task})

@login_required
@user_passes_test(is_superadmin)
def task_reports_superadmin(request):
    tasks = Task.objects.filter(status='Completed')
    return render(request, 'superadmin/task_reports.html', {'tasks': tasks})