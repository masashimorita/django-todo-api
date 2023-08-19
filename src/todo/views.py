"""
Views for the todo API
"""
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import (
    TodoList,
)
from todo.serializers import (
    TodoListSerializer
)


class TodoListsView(APIView):
    """API for listing & creating todo lists."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, requet, format=None):
        """Retrieve todo lists for authenticated user."""
        todo_lists = TodoList.objects.filter(
            user=self.request.user
        ).order_by('-id')
        serializer = TodoListSerializer(todo_lists, many=True)
        return Response(serializer.data)
