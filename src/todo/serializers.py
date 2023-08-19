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
