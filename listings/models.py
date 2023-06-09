from django.db import models
from .crypto import generate_key,PasswordManager,password_encode,generate_pass
from .password import generate_password
from django.contrib.auth import get_user_model
import zlib
import base64

class Service(models.Model):

    categories = (("work","work"),("priority","priority"),("entertainment","entertainment"),("others","others"),("games","games"),("education","education"))

    service_name = models.CharField(max_length=255,unique=True)
    password_hashed = models.TextField(blank=True)
    verify_hashed = models.CharField(max_length=255,default="",blank=True)
    key = models.CharField(max_length=200,blank=True)
    date_created = models.DateTimeField(auto_now=True)
    passphrase = models.TextField()
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    link = models.URLField(max_length=255)
    email = models.EmailField(blank=True,max_length=255,null=True)
    category = models.CharField(max_length=255,choices=categories,blank=True,null=True)
    login = models.CharField(max_length=255,null=True,blank=True)
    image = models.TextField(max_length=255,null=True,blank=True)
    score = models.IntegerField(null=True, blank=True,default=75)

    
    def save(self,*args,**kwargs):
        
        
        self.key = generate_key(self.user.master_password)
        self.password_hashed = base64.b64encode( zlib.compress(bytes(password_encode(self.password_hashed,self.key),'utf-8'),4) ).decode()

        super(Service,self).save(*args,**kwargs)



    def __str__(self) -> str:
        return self.service_name +" created at "+str(self.date_created)
