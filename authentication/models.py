from django.db import models
from django.contrib.auth.models import AbstractUser
from listings.crypto import PasswordManager
from django.contrib.auth.hashers import make_password

# Create your models here.
def user_directory_path(instance, filename):
    # function to return a path that includes the user's username as a subdirectory
    return 'media/profile_pictures/{0}/{1}'.format(instance.user.username, filename)


class User(AbstractUser):

    profile = models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    master_password = models.CharField(max_length=255,blank=True)
    changed = models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return self.username   
    
    def save(self,*args,**kwargs):
        if not self.changed:
            self.master_password = self.password
            self.password = make_password(self.password)
            manager = PasswordManager()
            self.master_password = manager.encrypt(self.master_password)
            self.changed = True
        super(User, self).save(*args,**kwargs)