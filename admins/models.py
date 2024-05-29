from django.db import models
from django.contrib.auth import models as authModels

# Create your models here.


class Admins(models.Model):
    username = models.CharField('帐号' , max_length = 50,default='') 
    pwd = models.CharField('密码' , max_length = 128,default='') 


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'admins'
        verbose_name = '管理员'  #单数形式
        verbose_name_plural = verbose_name #复数形式





