from django.db import models
from django.contrib.auth import models as authModels

# Create your models here.


class Banji(models.Model):
    banjimingcheng = models.CharField('班级名称' , max_length = 255,default='') 


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'banji'
        verbose_name = '班级'  #单数形式
        verbose_name_plural = verbose_name #复数形式





