"""
Views for the todo API
"""
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from drf_spectacular.utils import extend_schema

from core.models import (
    TodoList,
)
from todo.serializers import (
    TodoListSerializer,
    TodoListDetailSerializer,
)


class TodoListsView(APIView):
    """API for listing & creating todo lists."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoListSerializer

    @extend_schema(responses={200: TodoListSerializer(many=True)})
    def get(self, request, format=None):
        """Retrieve todo lists for authenticated user."""
        todo_lists = TodoList.objects.filter(
            user=request.user
        ).order_by('-id')
        serializer = TodoListSerializer(todo_lists, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses={
            201: TodoListSerializer,
            400: Response
        },
    )
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


class TodoListDetailView(APIView):
    """API for get, update and delete a todo list."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoListDetailSerializer

    def get_object(self, pk):
        """Retrieve todo list object by ID."""
        todo_list = get_object_or_404(TodoList, pk=pk, user=self.request.user)
        return todo_list

    @extend_schema(
        responses={
            201: TodoListDetailSerializer,
            404: Response
        },
    )
    def get(self, request, pk, format=None):
        """Retrieve todo list object detail."""
        todo_list = self.get_object(pk=pk)
        serializer = TodoListDetailSerializer(todo_list)
        return Response(serializer.data)

    @extend_schema(
        responses={
            200: TodoListDetailSerializer,
            400: Response,
            404: Response
        },
    )
    def put(self, request, pk, format=None):
        """Update a todo list."""
        todo_list = self.get_object(pk=pk)
        serializer = TodoListDetailSerializer(
            todo_list,
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: None,
            404: Response
        },
    )
    def delete(self, request, pk, format=None):
        """Delete a todo list in database."""
        todo_list = self.get_object(pk=pk)
        todo_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
