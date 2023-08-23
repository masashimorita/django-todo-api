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
    Task,
)
from todo.serializers import (
    TodoListSerializer,
    TodoListDetailSerializer,
    TaskSerializer
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


class TasksView(APIView):
    """API for get and create a task for the todo list."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get_todo_list(self, pk):
        """Retrieve todo list object by ID."""
        todo_list = get_object_or_404(TodoList, pk=pk, user=self.request.user)
        return todo_list

    @extend_schema(responses={200: TaskSerializer(many=True)})
    def get(self, request, todo_list_id, format=None):
        """Retrieve list of tasks for the todo list."""
        todo_list = self.get_todo_list(pk=todo_list_id)
        tasks = Task.objects.filter(todo_list=todo_list).order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            201: TaskSerializer,
            400: Response
        },
    )
    def post(self, request, todo_list_id, format=None):
        """Create a task for the todo list."""
        todo_list = self.get_todo_list(pk=todo_list_id)

        given_data = request.data
        given_data['todo_list'] = todo_list
        serializer = TaskSerializer(
            data=given_data,
            context={"request": request}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    """API for get, update and delete a task."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get_object(self, todo_list_id, pk):
        """Retrieve task object by ID"""
        todo_list = get_object_or_404(
            TodoList,
            pk=todo_list_id,
            user=self.request.user
        )
        task = get_object_or_404(Task, pk=pk, todo_list=todo_list)
        return task

    def get(self, request, todo_list_id, pk, format=None):
        """Retrieve a task in todo list."""
        task = self.get_object(todo_list_id, pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, todo_list_id, pk, format=None):
        """Update a task in todo list."""
        task = self.get_object(todo_list_id, pk)
        serializer = TaskSerializer(
            task,
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, todo_list_id, pk, format=None):
        """Delete a task in todo list."""
        task = self.get_object(todo_list_id, pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
