"""
Serializers for the todo API view
"""
from rest_framework import serializers

from core.models import (
    TodoList,
    Task,
)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task object."""

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'content', 'completed',
            'deadline', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        depth = 1


class TodoListSerializer(serializers.ModelSerializer):
    """Serializer for TodoList object."""

    class Meta:
        model = TodoList
        fields = ['id', 'label', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create a todo list"""
        todo_list = TodoList.objects.create(
            user=self.context['request'].user,
            **validated_data,
        )
        return todo_list


class TodoListDetailSerializer(TodoListSerializer):
    """Serializer for TodoList object detail."""
    tasks = TaskSerializer(read_only=True, many=True, source='task_set')

    class Meta(TodoListSerializer.Meta):
        fields = TodoListSerializer.Meta.fields + ['tasks']
        read_only_fields = TodoListSerializer.Meta.read_only_fields + ['tasks']
