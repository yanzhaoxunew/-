from django.db import models


# Create your models here.
class OrderDetail(models.Model):
    name = models.CharField(max_length=32, verbose_name='报餐人')
    date = models.DateField(verbose_name='报餐时间')
    breakfast = models.BooleanField(null=True, blank=False,default=False)
    lunch = models.BooleanField(null=True, blank=False,default=False)
    dinner = models.BooleanField(null=True, blank=False,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('date','name')
        verbose_name_plural = '报餐详情表'
    def __str__(self):
        return f"{self.name}-{self.date}"

class UserList(models.Model):
    name = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural='成员表'
    def __str__(self):
        return self.name
