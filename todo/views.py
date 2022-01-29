from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import TodoList
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
