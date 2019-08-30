from django.db import models
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from mptt.models import TreeForeignKey, MPTTModel


# Create your models here.
class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '标签'

    @classmethod
    def get_navs(cls) -> dict:
        """获取导航栏标签与普通标签"""
        navs = []
        normal_tags = []
        tags = cls.objects.filter(status=cls.STATUS_NORMAL)
        # 不要将is_nav字段分别用两个子query_set查询，这样会造成两次IO
        for tag in tags:
            if tag.is_nav == True:
                navs.append(tag)
            else:
                normal_tags.append(tag)
        return {
            'navs': navs,
            'normal_tags': normal_tags
        }


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    tag = models.ManyToManyField(to=Tag, verbose_name='标签')
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=255, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为Markdown格式')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL,
                                         verbose_name='状态')
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(verbose_name='页面访问量', default=0)
    uv = models.PositiveIntegerField(verbose_name='独立访问用户数', default=0)
    send_subscriber = models.BooleanField(default=False, verbose_name='已经发布给订阅者')

    # TODO:删除分类功能，与标签重合，并将评论绑定至文章，取消评论通用化，

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = '文章'
        ordering = ['-created_time'] # 根据id降序排列

    @staticmethod
    def get_by_tag_id(tag_id):
        """根据tag_id查找文章"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
            tag = None
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner')
        return post_list, tag

    @classmethod
    def get_latest(cls):
        """返回最新的5篇文章"""
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')[:5]

    @classmethod
    def get_hot(cls):
        """返回最热门的5篇文章"""
        return cls.objects.filter(status=cls.STATUS_NORMAL).only('title', 'id').order_by('-pv')[:5]


    @cached_property
    def tags(self):
        """返回所有标签的拼接名字"""
        return ','.join(self.tag.values_list('name', flat=True))

    @classmethod
    def get_unsent_to_subscriber_post(cls):
        return cls.objects.filter(send_subscriber=False).prefetch_related('tag')\
            .defer('created_time', 'content', 'status', 'owner', 'pv', 'uv')


class Comment(MPTTModel):
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    target_post = models.ForeignKey(to=Post, on_delete=models.CASCADE, verbose_name='评论文章')
    email = models.EmailField(verbose_name='邮箱', null=True, default=None)
    url = models.URLField(blank=True, null=True, default=None, verbose_name='个人网站')
    content = models.CharField(max_length=500, verbose_name='评论内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    parent = TreeForeignKey(
        to='self',
        on_delete=models.CASCADE,
        verbose_name='父级评论',
        blank=True,
        null=True,
        default=None,
        related_name='children'
    )
    reply_to = models.CharField(max_length=20, blank=True, null=True, verbose_name='回复对象', default=None)

    class Meta:
        verbose_name_plural = verbose_name = '评论'
        ordering = ['-created_time']

    @classmethod
    def get_latest(cls):
        """获取最新的5条评论"""
        return cls.objects.all().order_by('-created_time')[:5]

