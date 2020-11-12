from django.db import models
from django.db import models
import datetime
from colorful.fields import RGBColorField
from ckeditor_uploader.fields import RichTextUploadingField


class User(models.Model):
    fname=models.CharField(verbose_name='نام',max_length=255,null=False)
    lname=models.CharField(verbose_name='نام خانوادگی',max_length=255,null=False)
    email=models.EmailField(verbose_name='ایمیل',null=False,unique=True)
    password=models.CharField(verbose_name='گذرواژه',max_length=255)
    photo=models.ImageField(upload_to='users/photos/',default='user-photo.png',verbose_name='عکس پروفایل',null=True,blank=True)
    def __str__(self):
        return "{} {}".format(self.fname,self.lname)
    @property
    def filee_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url  
class Yadd(models.Model):
    content=RichTextUploadingField(config_name='custom',verbose_name='متن یادداشت')
    date=models.DateTimeField(verbose_name='تاریخ')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title