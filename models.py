from django.db import models
import os
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from datetime import datetime, date, timedelta
'''
def compress(image):
    im = Image.open(image)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image
'''
class OverwriteStorage(FileSystemStorage):
    
    def get_available_name(self, name,max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
# Create your models here.

class Post(models.Model):
    title= models.CharField(max_length=300)
    date= models.DateField(null=True)
    time= models.TimeField(null=True,blank=True) 
    img = models.ImageField(upload_to='img/%m-%y',storage=OverwriteStorage,default=False,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField('Approved',default=False)
    reportpdf = models.FileField(upload_to = 'report/',storage=OverwriteStorage,default=False)
    report = models.BooleanField('report',default=False)
    cllg = models.CharField(max_length=200,default=False)
    venue = models.CharField(max_length=200,default=False)
    dept = models.CharField(max_length=100,default=True)
    etype = models.CharField(max_length=300,null=True,blank=True)
    pay =   models.IntegerField(null=True)
    description = models.CharField(max_length=300,default=True)
    reglink = models.CharField(max_length=300,default=True)
    is_archive = models.BooleanField('is_archive',default=False)
    closed = models.BooleanField('closed',default=False)
    '''
    def save(self, *args, **kwargs):
        new_image = compress(self.img)
        self.img = new_image
        super().save(*args, **kwargs)
    '''

    class Meta:
        ordering = ['-created']

    
    def __str__(self):
        return self.title




class UserReg(models.Model):
    name= models.CharField(max_length=300)
    email= models.EmailField(null=False,blank=False,default=False)
    cllgname= models.CharField(max_length=300)
    sors =  models.CharField(max_length=100)
    verify = models.ImageField(upload_to="users/%m-%y",null=True,blank=True)
    event = models.CharField(max_length=300,default=False)
    fromcllg = models.CharField(max_length=300,default=False)
    def __str__(self):
        return self.name









