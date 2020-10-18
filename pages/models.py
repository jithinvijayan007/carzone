from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Car(models.Model):
    Service_Choices=[('Platinum','Platinum'),('Gold','Gold')]
    car_model=models.CharField(max_length=100)
    car_owner=models.CharField(max_length=100)
    car_notes=models.CharField(max_length=100)
    car_number=models.CharField(max_length=100)
    description=models.TextField()
    service_type=models.CharField(max_length=10,choices=Service_Choices,blank=True)
    submission_date=models.DateField()
    year_old=models.CharField(max_length=20,null=True)
    servicing=models.ManyToManyField('Service',blank=True)

    def __str__(self):
        return self.car_model +"     "+self.car_owner

class Service(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Mob_Number=models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

    

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

