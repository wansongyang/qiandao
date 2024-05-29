from django.db import models
from django.contrib.auth import models as authModels

# Create your models here.
 


class Qiandaoxinxi(models.Model):
    qiandaobianhao = models.CharField('签到编号' , max_length = 50,default='') 
    qiandaobanji = models.IntegerField('签到班级',default=0) 
    qiandaomingcheng = models.CharField('签到名称' , max_length = 255,default='') 
    qiandaoshijian = models.CharField('签到时间' , max_length=19,default='' ) 
    jiezhishijian = models.CharField('截止时间' , max_length=19,default='' ) 
    shuoming = models.CharField('说明' , max_length = 255,default='') 
    faburen = models.CharField('发布人' ,db_column='faburen' , max_length=50,default='') 


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'qiandaoxinxi'
        verbose_name = '签到信息'  #单数形式
        verbose_name_plural = verbose_name #复数形式





