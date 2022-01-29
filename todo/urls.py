from django.urls import path
from todo import views

app_name = 'todo'
urlpatterns = [
    path('lists/', views.TodoListView.as_view(), name='todolist-list'),
    path(
        'lists/<int:pk>/',
        views.TodoListDetailView.as_view(),
        name='todolist-detail'
    ),
    path(
        'lists/<int:todo_list_pk>/tasks/',
        views.TodoTaskListView.as_view(),
        name='todotask-list'
    ),
    path(
        'lists/<int:todo_list_pk>/tasks/<int:pk>/',
        views.TodoTaskDetailView.as_view(),
        name='todotask-detail'
    ),
]
