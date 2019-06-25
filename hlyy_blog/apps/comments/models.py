from django.db import models

from blog.models import Post


class Comments(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    target = models.CharField(max_length=200, verbose_name='评论对象')
    content = models.CharField(max_length=2000, verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    website = models.URLField(verbose_name='网站', blank=True)
    email = models.EmailField(verbose_name='邮箱', blank=True)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL,
                                         verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = verbose_name = '评论'

    @classmethod
    def get_by_target(cls, target):
        """通过URL的path部分返回对象的评论"""
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)
