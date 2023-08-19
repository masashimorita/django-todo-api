"""
Serializers for the todo API view
"""
from rest_framework import serializers

from core.models import (
    TodoList,
)


class TodoListSerializer(serializers.ModelSerializer):
    """Serializer for TodoList object."""

    class Meta:
        model = TodoList
        fields = ['id', 'label']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a todo list"""
        todo_list = TodoList.objects.create(
            user=self.context['request'].user,
            **validated_data,
        )
        return todo_list
