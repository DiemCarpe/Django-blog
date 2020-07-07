from django import template
from ..models import Post,Category,Tag

register=template.Library()
"""

导入 template 这个模块，然后实例化了一个 template.Library 类
并将函数 show_recent_posts 装饰为 register.inclusion_tag
这样就告诉 django，这个函数是我们自定义的一个类型为 inclusion_tag 的模板标签

"""

@register.inclusion_tag('blog/inclusions/_weather.html')
def show_weather():
    """
    天气模板

    """
    pass


@register.inclusion_tag('blog/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):
    """
    最新文章模板标签

    """
    return {
        # 'recent_post_list':Post.objects.all().order_by('-create_time')[:num],
        'recent_post_list':Post.objects.all()[:num],
    }



@register.inclusion_tag('blog/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    """
    归档模板标签

    这里 Post.objects.dates 方法会返回一个列表
    列表中的元素为每一篇文章（Post）的创建时间（已去重）
    且是 Python 的 date 对象，精确到月份，降序排列
    接受的三个参数值表明了这些含义，一个是 created_time 即 Post 的创建时间
    month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）

    """
    return {
        'archives_list': Post.objects.dates('create_time','year',order='DESC'),
    }




@register.inclusion_tag('blog/inclusions/_categories.html',takes_context=True)

def show_categories(context):
    """
    分类模板标签

    """
    return{
        'categories_list':Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_tag.html',takes_context=True)
def show_tag(context):
    """
    标签云模板标签

    """
    return{
        'tag_list':Tag.objects.all(),
    }

