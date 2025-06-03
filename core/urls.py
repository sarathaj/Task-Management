
from django.urls import path
from .views import (
    TaskListView, TaskUpdateView, TaskReportView,
    admin_dashboard, task_reports
)
urlpatterns = [
    # API endpoints
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:id>/report/', TaskReportView.as_view(), name='task-report'),

    # Admin panel HTML views
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/task-reports/', task_reports, name='task-reports'),
]
