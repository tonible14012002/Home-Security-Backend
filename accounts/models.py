from django.db import models
from django.contrib.auth.models import (
    AbstractUser, 
    UserManager, 
)
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone

# Create your models here.

def user_directory_path(instance, filename):
    return f'{instance.username}/{filename}'

# model Manager
class AdminUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)
    
class OrdinaryUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False, is_superuser=False)

# user model
class MyUser(AbstractUser):
    
    image = models.ImageField(upload_to=user_directory_path, 
                              blank=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=False)
    
    address = models.CharField(max_length=200, blank=False)
    birth = models.DateField(default=timezone.now, 
                                 null=False, blank=False)

    phone = models.CharField(max_length=15,
                             validators=[
                                 MinLengthValidator(9),
                                 RegexValidator(
                                     r'(84|0[3|5|7|8|9])+([0-9]{8})\b',
                                     message='Enter valid phone number')
                                 ])
    
    objects = UserManager()
    is_admin = AdminUserManager()
    is_ordinary = OrdinaryUserManager()
    
    class Meta:
        ordering = ('-updated_at', '-created_at')
        unique_together = ('phone', 'email')
        
    def __str__(self):
        return self.get_full_name()

    def total_visit(self):
        return self.visits.count()

class Visit(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, 
                             on_delete=models.CASCADE, 
                             related_name='visits')
    class Meta:
        ordering = ('time',)

