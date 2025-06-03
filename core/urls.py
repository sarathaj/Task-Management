
from django.urls import path
from .views import (
    TaskListView, TaskUpdateView, TaskReportView,
    admin_dashboard, task_reports, assign_task,
    create_user, edit_user, delete_user,
    create_task, edit_task, delete_task, task_reports_superadmin,
    superadmin_dashboard, manage_users, manage_tasks, role_based_redirect 
)
urlpatterns = [
    # API endpoints
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:id>/report/', TaskReportView.as_view(), name='task-report'),
    path('role-redirect/', role_based_redirect, name='role-redirect'),

    # Admin panel HTML views
    path('admin/assign-task/', assign_task, name='assign-task'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/task-reports/', task_reports, name='task-reports'),

    # SuperAdmin panel
    path('superadmin/dashboard/', superadmin_dashboard, name='superadmin-dashboard'),
    path('superadmin/users/', manage_users, name='manage-users'),
    path('superadmin/tasks/', manage_tasks, name='manage-tasks'),

    # superadmin User/admin management
    path('superadmin/users/create/', create_user, name='create-user'),
    path('superadmin/users/<int:id>/edit/', edit_user, name='edit-user'),
    path('superadmin/users/<int:id>/delete/', delete_user, name='delete-user'),

    # superadmin task management
    path('superadmin/tasks/create/', create_task, name='create-task'),
    path('superadmin/tasks/<int:id>/edit/', edit_task, name='edit-task'),
    path('superadmin/tasks/<int:id>/delete/', delete_task, name='delete-task'),
    path('superadmin/task-reports/', task_reports_superadmin, name='superadmin-task-reports'),
]
