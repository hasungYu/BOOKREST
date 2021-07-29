from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from .choices import *

# Create your models here.
class UserManager(BaseUserManager):    
    use_in_migrations = True    
   
    #유저 생성
    #파라미터로 전달받은 값들을 user 객체로 db에 저장한다
    def create_user(self, email, username, password, **extra_fields):   
        if not email:            
            raise ValueError('이메일을 반드시 입력해주세요.')
        if not password:            
            raise ValueError('비밀번호를 반드시 입력해주세요.')    
        email = self.normalize_email(email)
        user = self.model(email = email, username=username, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)        
        return user

    #슈퍼 유저
    def create_superuser(self, email, username, password):        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)        
        return user


    # def create_user(self, email, username, password=None, **extra_fields):   
    #     if not email:
    #         raise ValueError("이메일은 필수 항목입니다.")
    #     if not username: 
    #         raise ValueError("이름은 필수 항목입니다.")

    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     email = self.normalize_email(email)
    #     user = self.model(email = email, username=username, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)        
    #     return user
    # #슈퍼 유저
    # def create_superuser(self, email, username, password):
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         password=password,
    #         username=username
    #     )
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)        
    #     return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
   
    objects = UserManager()
    #user_id = models.BigIntegerField(primary_key=True,null=False)
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=20, unique=True, null=True)
    major = models.CharField(choices=MAJOR, max_length=30, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    birth = models.DateField('birth', null=True)
    student_id = models.CharField(max_length=20, null=True)
    #no_borrow_period
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

#    @property
#    def is_staff(self):
#        return self.is_superuser
