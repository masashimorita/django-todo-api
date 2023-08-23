"""
Test for the Todo API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import (
    TodoList,
    Task,
)

from todo.serializers import (
    TodoListSerializer,
    TodoListDetailSerializer,
    TaskSerializer,
)


TODO_LIST_URL = reverse('todo:todo-lists')


def detail_url(todo_list_id):
    """Create and return a todo list detail URL."""
    return reverse('todo:todo-list-detail', args=[todo_list_id])


def create_user(email='test@example.com', password='password123', **params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password, **params)


def create_todo_lsit(user, label='Sample List'):
    """Create and return a new todo list"""
    return TodoList.objects.create(user=user, label=label)


def create_task(todo_list, **params):
    """Create and return a new task"""
    return Task.objects.create(todo_list=todo_list, **params)


class PublicTodoAPITests(TestCase):
    """Test unauthenticated API request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TODO_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_todo_lists(self):
        """Test retrieving a lsit of todo lists."""
        create_todo_lsit(user=self.user, label='List 001')
        create_todo_lsit(user=self.user, label='List 002')

        res = self.client.get(TODO_LIST_URL)

        todo_lists = TodoList.objects.all().order_by('-id')
        serializer = TodoListSerializer(todo_lists, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_todo_list_limited_to_user(self):
        """Test list of todo lists is limited to authenticated user."""
        other_user = create_user(email='other@example.com')
        create_todo_lsit(user=other_user, label='List 001')
        create_todo_lsit(user=self.user, label='List 002')

        res = self.client.get(TODO_LIST_URL)

        todo_lists = TodoList.objects.filter(user=self.user).order_by('-id')
        serializer = TodoListSerializer(todo_lists, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_todo_list(self):
        """Test creating a todo list"""
        payload = {'label': 'Sample List'}
        res = self.client.post(TODO_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TodoList.objects.filter(id=res.data['id']).exists())
        todo_list = TodoList.objects.get(id=res.data['id'])
        self.assertEqual(todo_list.user, self.user)

    def test_retrieve_todo_list_by_pk(self):
        """Test retrieving a todo list with pk."""
        todo_list = create_todo_lsit(user=self.user)
        task = create_task(todo_list=todo_list, name='Sample Task')
        url = detail_url(todo_list_id=todo_list.id)

        res = self.client.get(url)

        serializer = TodoListDetailSerializer(todo_list)
        task_serializer = TaskSerializer(task)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertIn(task_serializer.data, serializer.data['tasks'])

    def test_update_todo_list(self):
        """Test updating a todo list."""
        todo_list = create_todo_lsit(user=self.user)
        payload = {'label': 'Shopping'}
        url = detail_url(todo_list_id=todo_list.id)

        res = self.client.put(url, payload)

        todo_list.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(todo_list.label, payload['label'])

    def test_delete_todo_list(self):
        """Test deleting a todo list."""
        todo_list = create_todo_lsit(user=self.user)
        task = create_task(todo_list=todo_list, name='Sample Task')
        url = detail_url(todo_list_id=todo_list.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TodoList.objects.filter(id=todo_list.id).exists())
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_todo_list_other_user_error(self):
        """Test trying to delete other users todo list gives error."""
        other_user = create_user(email='other@example.com')
        todo_list = create_todo_lsit(user=other_user)
        task = create_task(todo_list=todo_list, name='Sample Task')
        url = detail_url(todo_list_id=todo_list.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(TodoList.objects.filter(id=todo_list.id).exists())
        self.assertTrue(Task.objects.filter(id=task.id).exists())
