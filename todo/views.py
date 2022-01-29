from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import TodoList, TodoTask
from todo import serializers


class TodoListView(generics.ListCreateAPIView):
    """List and Create TodoList"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = TodoList.objects.all()
    serializer_class = serializers.TodoListSerializer

    def get_queryset(self):
        """Return objects for  the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new TodoList"""
        serializer.save(user=self.request.user)


class TodoListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage Todo List"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = TodoList.objects.all()
    serializer_class = serializers.TodoListSerializer

    def get_queryset(self):
        """Return objects for  the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TodoTaskListView(generics.ListCreateAPIView):
    """List and Create TodoTask"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = TodoTask.objects.all()
    serializer_class = serializers.TodoTaskSerializer

    def todo_list_pk(self):
        """Get TodoList PK from request context"""
        kwargs = self.request.parser_context.get('kwargs')
        return kwargs['todo_list_pk']

    def get_queryset(self):
        """Return objects for  the current authenticated user only"""
        return self.queryset.filter(
            user=self.request.user,
            todo_list_id=self.todo_list_pk()
        ).order_by('priority')

    def perform_create(self, serializer):
        """Create a new todo task"""
        todo_list = TodoList.objects.get(
            id=self.todo_list_pk(),
            user=self.request.user
        )
        serializer.save(user=self.request.user, todo_list=todo_list)


class TodoTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """List and Create TodoTask"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = TodoTask.objects.all()
    serializer_class = serializers.TodoTaskSerializer

    def todo_list_pk(self):
        """Get TodoList PK from request context"""
        kwargs = self.request.parser_context.get('kwargs')
        return kwargs['todo_list_pk']

    def get_queryset(self):
        """Return objects for  the current authenticated user only"""
        return self.queryset.filter(
            user=self.request.user,
            todo_list_id=self.todo_list_pk()
        ).order_by('priority')
