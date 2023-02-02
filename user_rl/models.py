from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from userdetails.models import Designation, Payroll


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2 = None):
        if not email:
            raise ValueError('Users must have an email address')
        # if not faces:
        #     faces=fc.face_store('name')
        #     return faces

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            # faces=faces
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,password=None):

        user = self.create_user(
            email,
            password=password,
            name= name,
            # faces=faces
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = id
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=100,null=True)
    pan_no = models.BigIntegerField(null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, default=None, null=True)
    payroll = models.OneToOneField(Payroll,on_delete=models.CASCADE, default=None, null=True)
    # faces = models.FileField(upload_to='/static')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identified = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name','faces']
    REQUIRED_FIELDS = ['name']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Attendance(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    time_stamp = models.DateTimeField(default=None)
    is_late = models.BooleanField()
    is_early = models.BooleanField()
    image = models.ImageField()

