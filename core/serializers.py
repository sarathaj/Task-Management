
from rest_framework import serializers
from .models import Task, User
from django.contrib.auth import get_user_model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['assigned_to']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'Completed':
            if not data.get('completion_report') or not data.get('worked_hours'):
                raise serializers.ValidationError("Completion report and worked hours are required when marking a task as completed.")
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role']
