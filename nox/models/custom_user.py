from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.forms import ModelForm
from localflavor.us.models import PhoneNumberField
from localflavor.us.forms import USPhoneNumberField
from south.modelsinspector import add_introspection_rules
from back_end.settings import USE_S3, STATICFILES_DIRS
from storages.backends.s3boto import S3BotoStorage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from nox.util import Util
import os

add_introspection_rules([], ["^localflavor\.us\.models\.PhoneNumberField"])

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
    def get_upload_location(instance, filename):
        extension = os.path.splitext(filename)[-1]
        prefix = Util.random_filename()
        filename = "%s%s" % (prefix, extension)
        return "user/%s/%s" % (instance.id, filename)
        
    storage = S3BotoStorage() if USE_S3 else None
    
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True, null=True)
    icon = models.ImageField(storage=storage, upload_to=get_upload_location, null=True)
 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
 
    objects = CustomUserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
 
    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        last_name = ' %s' % (self.last_name) if self.last_name else ''
        return "%s%s" % (self.first_name, last_name)
 
    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.first_name
    
    def get_default_icon(self):
        return "user/default.jpg"
 
    def __unicode__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?
        return True
 
    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?
        return self.is_admin
    
    class Meta:
        db_table = "custom_user"
        app_label = "nox"
        
class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'phone_number']