from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'assigned_admin', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles & Assignment', {'fields': ('role', 'assigned_admin')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'assigned_admin', 'password1', 'password2'),
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'due_date', 'worked_hours')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'assigned_to__username')
    ordering = ('-due_date',)
    autocomplete_fields = ['assigned_to']
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Assignment', {'fields': ('assigned_to', 'due_date', 'status')}),
        ('Completion', {'fields': ('completion_report', 'worked_hours')}),
    )