import mistune
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Category(models.Model):
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
        verbose_name_plural = verbose_name = '分类'

    @classmethod
    def get_navs(cls) -> dict:
        """获取导航栏分类与普通分类"""
        navs = []
        normal_categories = []
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        # 不要将is_nav字段分别用两个子query_set查询，这样会造成两次IO
        for category in categories:
            if category.is_nav == True:
                navs.append(category)
            else:
                normal_categories.append(category)
        return {
            'navs': navs,
            'normal_categories': normal_categories
        }

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL,
                                         verbose_name='状态')
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '标签'

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=255, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为Markdown格式')
    content_html = models.TextField(verbose_name='HTML正文', editable=False, blank=True)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL,
                                         verbose_name='状态')
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='分类')
    tag = models.ManyToManyField(to=Tag, verbose_name='标签')
    pv = models.PositiveIntegerField(verbose_name='页面访问量', default=0)
    uv = models.PositiveIntegerField(verbose_name='独立访问用户数', default=0)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = '文章'
        ordering = ['-id'] # 根据id降序排列

    @staticmethod
    def get_by_tag_id(tag_id):
        """根据tag_id查找文章"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
            tag = None
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')
        return post_list, tag

    @staticmethod
    def get_by_category_id(category_id):
        """根据category_id查找文章"""
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')
        return post_list, category

    @classmethod
    def get_latest(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).\
            select_related('owner').prefetch_related('tag').order_by('-created_time')

    @classmethod
    def get_hot(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    def save(self, **kwargs):
        # 将正文转换为markdown并保存至content_html字段中
        self.content_html = mistune.markdown(self.content)
        super().save(**kwargs)




