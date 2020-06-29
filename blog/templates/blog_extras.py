from django import template
from ..models import Post,Category,Tag

register=template.Library()

@register.inclusion_tag()
def show_recent_posts(context,num=5):
    return {
        'recent_post_list':Post.objects.all().order_by('-create_time')[:num],
    }

