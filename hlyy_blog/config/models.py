from django.db import models
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
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

class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏')
    )
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    )

    title = models.CharField(max_length=50, verbose_name='标题')
    display_type = models.PositiveSmallIntegerField(choices=SIDE_TYPE, default=1, verbose_name='展示类型')
    content = models.CharField(max_length=500, blank=True, verbose_name='内容', help_text='如果不为HTML，则可以为空')
    status = models.PositiveSmallIntegerField(choices=STATUS_ITEMS, default=STATUS_SHOW, verbose_name='状态')
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = verbose_name = '侧边栏'

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    def content_to_html(self):
        """将内容渲染成HTML"""
        # 避免循环引用
        from blog.models import Post
        from comments.models import Comments
        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.get_latest()
            }
            return render_to_string('config/blocks/sidebar_posts.html',
                                    context=context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.get_hot()
            }
            return render_to_string('config/blocks/sidebar_posts.html',
                                    context=context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                'comments': Comments.objects.filter(status=Comments.STATUS_NORMAL)
            }
            return render_to_string('config/blocks/sidebar_comments.html',
                                    context=context)


