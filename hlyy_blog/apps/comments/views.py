from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    template_name = 'comments/results.html'
    http_method_names = ['post']
    def post(self, request):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        if comment_form.is_valid():
            # CommentForm中没有包含target字段，因为该字段不需要渲染成HTML
            comment = comment_form.save(commit=False)
            comment.target = target
            comment.save()
            succeed = True
        else:
            succeed = False
        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target
        }
        return self.render_to_response(context)

