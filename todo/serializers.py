from rest_framework import serializers
from core.models import TodoList, TodoTask


class TodoListSerializer(serializers.ModelSerializer):
    """Serializer for TodoList"""

    class Meta:
        model = TodoList
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TodoTaskSerializer(serializers.ModelSerializer):
    """Serializer for TodoTask"""

    class Meta:
        model = TodoTask
        fields = ('id', 'title', 'priority', 'is_completed', 'note')
        read_only_fields = ('id',)
