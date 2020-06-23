from django.db import models

class OperationRecord(models.Model):
     name = models.CharField('操作名称',max_length=20)
     time = models.DateTimeField('操作时间',auto_now_add=True)
     value = models.BooleanField('操作值')

