import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, admin_id):
        if not email:
            raise ValueError("User must have a email address")

        if not first_name:
            raise ValueError("User must have a first name")

        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            admin_id = admin_id
        )

        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name, admin_id):
        
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            first_name = first_name,
            last_name = last_name,
            admin_id = admin_id
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user

class Account(AbstractBaseUser):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField(verbose_name = "email", max_length = 200, unique = True)
    date_joined = models.DateTimeField(verbose_name = 'date joined', auto_now_add = True)
    last_login = models.DateTimeField(verbose_name = 'last login', auto_now = True)
    is_admin = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)
    admin_id = models.UUIDField(null=True, editable = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    first_name = models.CharField(verbose_name = "first name", max_length = 30)
    last_name = models.CharField(verbose_name = "last name", max_length = 30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def create(self, validated_data):
        return Account.objects.create(**validated_data)