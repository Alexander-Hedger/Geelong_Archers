from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first_name")
        if not last_name:
            raise ValueError("Users must have a last_name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name='email',
                              max_length=100, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    archery_australia_id = models.IntegerField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='photos/users', blank=True, default='photos/users/user_placeholder.jpg')
    member_expiry = models.DateField(blank=True, null=True)
    division_choices = [
        ('Recurve', 'Recurve'),
        ('Compound', 'Compound'),
        ('Longbow', 'Longbow'),
        ('Barebow Recurve', 'Barebow Recurve'),
        ('Barebow Compound', 'Barebow Compound'),
        ('Crossbow', 'Crossbow'),
    ]
    archer_class_choices = [
        ('Cub', 'Cub'),
        ('Intermediate', 'Intermediate'),
        ('Cadet', 'Cadet'),
        ('20 & Under', '20 & Under'),
        ('Open', 'Open'),
        ('Master', 'Master'),
        ('Veteran', 'Veteran'),
        ('Veteran+', 'Veteran+'),
        ('Para Archer', 'Para Archer'),
        ('Vision Impaired', 'Vision Impaired'),
    ]

    division = models.CharField(
        max_length=20, choices=division_choices, default='Recurve')
    archer_class = models.CharField(
        max_length=20, choices=archer_class_choices, default='Open')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Committee(models.Model):
    position = models.CharField(
        max_length=40, unique=True, primary_key=True)
    member = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/users',
                              default='photos/users/user_placeholder.jpg')
    short_desc = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.position


class LifeMember(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    year_made = models.IntegerField(blank=True, null=True)
    date_active_start = models.CharField(max_length=10, blank=True, null=True)
    date_active_end = models.CharField(max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/users', blank=True, null=True)
    short_desc = models.CharField(max_length=250, blank=True, null=True)
    long_desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
