"""
Views for the todo API
"""
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

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
    serializer_class = TodoListSerializer

    @extend_schema(responses={200: TodoListSerializer(many=True)})
    def get(self, requet, format=None):
        """Retrieve todo lists for authenticated user."""
        todo_lists = TodoList.objects.filter(
            user=self.request.user
        ).order_by('-id')
        serializer = TodoListSerializer(todo_lists, many=True)
        return Response(serializer.data)

    @extend_schema(responses={201: TodoListSerializer})
    def post(self, request, format=None):
        """Create todo lists for authenticated user."""
        serializer = TodoListSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
