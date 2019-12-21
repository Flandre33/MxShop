from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    """
    用户信息
    """
    
