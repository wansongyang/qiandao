from django.db import models
from django.contrib.auth import models as authModels

# Create your models here.
XINGBIE_CHOICES = (
   ('男' , '男') , 
   ('女' , '女') , 

    )  
 


class Xuesheng(models.Model):
    xuehao = models.CharField('学号' , max_length = 50,default='') 
    mima = models.CharField('密码' , max_length = 128,default='') 
    xingming = models.CharField('姓名' , max_length = 50,default='') 
    xingbie = models.CharField('性别' , choices=XINGBIE_CHOICES , max_length=512,default='') 
    lianxidianhua = models.CharField('联系电话' , max_length = 50,default='') 
    suozaibanji = models.IntegerField('所在班级',default=0) 
    jianjie = models.TextField('简介',default='') 


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'xuesheng'
        verbose_name = '学生'  #单数形式
        verbose_name_plural = verbose_name #复数形式





