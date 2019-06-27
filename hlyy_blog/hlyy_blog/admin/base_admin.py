class BaseOwnerAdmin:
    """
    1，自动补充文章、分类等Model的owner字段
    2，过滤queryset，只显示当前登录用户的内容
    """
    exclude = ('owner',)

    def save_models(self):
        print('############################################')
        self.new_obj.owner = self.request.user
        return super().save_models()

    def get_list_queryset(self):
        qs = super().get_list_queryset()

        return qs.filter(owner=self.request.user)