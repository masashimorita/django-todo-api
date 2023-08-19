"""
URL mappings for the todo API
"""
from django.urls import path

from todo import views


app_name = 'todo'


urlpatterns = [
    path('', views.TodoListsView.as_view(), name='todo-lists')
]
