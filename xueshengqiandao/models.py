from django.db import models
from django.contrib.auth import models as authModels

# Create your models here.
 
SHIFOUCHIDAO_CHOICES = (
   ('未迟到' , '未迟到') , 
   ('迟到' , '迟到') , 

    )  


class Xueshengqiandao(models.Model):
    qiandaoxinxiid = models.IntegerField('签到信息id',default=0)  
    qiandaobianhao = models.CharField('签到编号' , max_length = 50,default='') 
    qiandaobanji = models.IntegerField('签到班级',default=0) 
    qiandaomingcheng = models.CharField('签到名称' , max_length = 255,default='') 
    qiandaoshijian = models.CharField('签到时间' , max_length=19,default='' ) 
    jiezhishijian = models.CharField('截止时间' , max_length=19,default='' ) 
    faburen = models.CharField('发布人' ,db_column='faburen' , max_length=50,default='') 
    xueshengqiandaoshijian = models.CharField('学生签到时间' , max_length=19,default='' ) 
    didian = models.CharField('地点' , max_length = 50,default='') 
    beizhu = models.TextField('备注',default='') 
    xueshengxingming = models.CharField('学生姓名' , max_length = 50,default='') 
    xueshengxuehao = models.CharField('学生学号' ,db_column='xueshengxuehao' , max_length=50,default='') 
    shifouchidao = models.CharField('是否迟到' , choices=SHIFOUCHIDAO_CHOICES , max_length=512,default='') 


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'xueshengqiandao'
        verbose_name = '学生签到'  #单数形式
        verbose_name_plural = verbose_name #复数形式





