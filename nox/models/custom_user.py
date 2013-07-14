from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=CustomUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
 
 
class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
 
    objects = CustomUserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
 
    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        return "%s %s" % (self.first_name, self.last_name)
 
    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.first_name
 
    def __unicode__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True
 
    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin
    
    class Meta:
        db_table = "custom_user"
        app_label = "nox"