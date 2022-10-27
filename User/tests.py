from django.test import TestCase
from .models import Users, Driver


class UserCreate(TestCase):
    def test_false_is_false(self):
        user = Users.objects.create_user(
            'email', 'first_name', 'last_name'
        )
        self.assertFalse(False)
