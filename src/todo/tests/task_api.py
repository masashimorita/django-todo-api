"""
Test for the Task API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from core.models import (
    TodoList,
    Task,
)

from todo.serializers import TaskSerializer


TASKS_URL = reverse('todo:tasks')


def detail_url(todo_list_id, task_id):
    """Create and return a todo list detail URL."""
    return reverse('todo:todo-list-detail', args=[todo_list_id, task_id])


def create_user(email='test@example.com', password='password123', **params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password, **params)


def create_todo_lsit(user, label='Sample List'):
    """Create and return a new todo list"""
    return TodoList.objects.create(user=user, label=label)


def create_task(todo_list, **params):
    """Create and return a new task"""
    return Task.objects.create(todo_list=todo_list, **params)


class PublicTaskAPITests(TestCase):
    """Test unauthenticated API request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TASKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskAPITest(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.todo_list = create_todo_lsit(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tasks(self):
        """Test retrieving a list of tasks."""
        create_task(todo_list=self.todo_list, name='Task 001')
        create_task(todo_list=self.todo_list, name='Task 002')

        res = self.client.get(TASKS_URL)

        tasks = Task.objects.filter(todo_list=self.todo_list).order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tasks_limited_to_todo_list(self):
        """Test list of task list is limited to authenticated user."""
        other_user = create_user(email='other@example.com')
        other_todo_list = create_todo_lsit(user=other_user)
        create_task(todo_list=other_todo_list, name='Task 001')
        create_task(todo_list=self.todo_list, name='Task 002')

        res = self.client.get(TASKS_URL)

        tasks = Task.objects.filter(todo_list=self.todo_list).order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_task(self):
        """Test creating a task in todo list."""
        payload = {
            'name': 'Shopping',
            'content': 'This is todo list for shopping items.',
            'deadline': timezone.now()
        }

        res = self.client.post(TASKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(id=res.data['id']).exists())
        task = Task.objects.get(id=res.data['id'])
        self.assertEqual(task.todo_list, self.todo_list)

    def test_retrieve_task_by_pk(self):
        """Test retrieving a task with pk."""
        task = create_task(todo_list=self.todo_list, name='Task 001')
        url = detail_url(task.todo_list, task.id)

        res = self.client.get(url)

        serializer = TaskSerializer(task)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_task(self):
        """Test updating a task."""
        task = create_task(todo_list=self.todo_list, name='Task 001')
        url = detail_url(task.todo_list, task.id)
        payload = {
            'name': 'MODIFIED',
            'content': 'THIS IS MODIFIED CONTENET',
            'completed': True,
            'deadline': timezone.now(),
        }

        res = self.client.put(url, payload)

        task.refresh_from_db()
        serializer = TaskSerializer(task)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.todo_list, self.todo_list)

    def test_delete_task(self):
        """Test deleting a task."""
        task = create_task(todo_list=self.todo_list, name='Task 001')
        url = detail_url(task.todo_list, task.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_task_other_user_todo_list_error(self):
        """Test trying to delete other users task in todo list"""
        other_user = create_user(email='other@example.com')
        todo_list = create_todo_lsit(user=other_user)
        task = create_task(todo_list=todo_list, name='Sample Task')
        url = detail_url(task.todo_list, task.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Task.objects.filter(id=task.id).exists())
