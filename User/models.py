from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(email, first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(email, first_name, last_name, password, True, True, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=255, unique=True, )
    first_name = models.CharField('Nombres', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)



    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Driver (models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    license = models.CharField('Licencia', max_length=255, blank=True, null=True)
    phone = models.CharField('Teléfono', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return f'{self.user} {self.license}'
