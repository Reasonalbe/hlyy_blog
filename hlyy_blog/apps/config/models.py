from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    title = models.CharField(max_length=50, verbose_name='标题')
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL,
                                         verbose_name='状态')
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1,6), range(1,6)),
                                         verbose_name='权重', help_text='权重越高展示越靠前')
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = verbose_name = '友链'

class Subscribe(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    email = models.EmailField(verbose_name='邮箱', db_index=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = verbose_name = '订阅'
