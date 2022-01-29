from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import TodoList, TodoTask


def sample_user(email='test@example.com', password='password', name='Test'):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name
    )


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name='TEST'
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='test123',
            name='TEST'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='test123',
                name='TEST'
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
            name='TEST'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_todo_list_str(self):
        """Test the todo_list string representation"""
        todo_list = TodoList.objects.create(
            user=sample_user(),
            name='Sample Todo List'
        )
        self.assertEqual(str(todo_list), todo_list.name)

    def test_todo_task_str(self):
        """Test the todo_task string representation"""
        user = sample_user()
        todo_list = TodoList.objects.create(user=user, name='Sample Todo List')
        todo_task = TodoTask.objects.create(
            user=user,
            todo_list=todo_list,
            title='Sample Task'
        )
        self.assertEqual(str(todo_task), todo_task.title)
