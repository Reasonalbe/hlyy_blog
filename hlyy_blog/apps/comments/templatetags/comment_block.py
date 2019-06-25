from django import template

from comments.forms import CommentForm
from comments.models import Comments


register = template.Library()
@register.inclusion_tag('comments/comment_block.html')
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comments.get_by_target(target)
    }