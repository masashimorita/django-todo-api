from django.urls import path
from todo import views

app_name = 'todo'
urlpatterns = [
    path('lists/', views.TodoListView.as_view(), name='todolist'),
    path('lists/<int:pk>/', views.TodoListDetailView.as_view(), name='todolist-detail')
]
