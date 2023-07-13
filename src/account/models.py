from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from config.models.TimeStampMixin import TimeStampMixin
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, phone, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')

        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if email is None:
            email = ''
        
        return self.create_user(phone, email, password, **extra_fields)

    def get_by_natural_key(self, phone):
        return self.get(phone=phone)


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):
    email = models.EmailField(max_length=100, unique=True)
    phone = PhoneNumberField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.phone}'
    
    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff


    # def send_activation_email(self, domain):
    #     async_task('account.tasks.send_activation_email_async', self.id, domain)

    #FIXME: further needed then make is_active false and verify it after conformations.
    def save(self, *args, **kwargs):
        if not self.pk:  # Only for newly created users
            self.is_active = True 
        super().save(*args, **kwargs)

    class Meta:
        default_manager_name = 'objects'
