import re
from django.shortcuts import render
from django.http import HttpResponse
from .models import  Post,Category,Tag
from django.shortcuts import  render,get_object_or_404
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def blog(request):
    # return render(request,'blog/_weather.html',context={
    #     'title':'我的博客首页',
    #     'he':'hah'
    # })
    post_list=Post.objects.all().order_by('-create_time')
    return render(request, 'blog/blog.html', context={'post_list':post_list})


def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    md=markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
        ])
    post.body=md.convert(post.body)
    m=re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)

    post.toc=m.group(1) if m is not None  else ''

    return render(request,'blog/detail.html',context={'post':post})



def archive(request,year,month):
    """
    使用了模型管理器（objects）的 filter 方法来过滤文章
    由于是按照日期归档，因此这里根据文章发表的年和月来过滤
    具体来说，就是根据 created_time 的 year 和 month 属性过滤
    筛选出文章发表在对应的 year 年和 month 月的文章
    注意这里 created_time 是 Python 的 date 对象，
    其有一个 year 和 month 属性，我们在 页面侧边栏：使用自定义模板标签 使用过这个属性。
    Python 中调用属性的方式通常是 created_time.year
    但是由于这里作为方法的参数列表，
    所以 django 要求我们把点替换成了两个下划线，即 created_time__year。
    同时和 index 视图中一样，我们对返回的文章列表进行了排序。
    此外由于归档页面和首页展示文章的形式是一样的，因此直接复用了 _weather.html 模板

    """
    post_list=Post.objects.filter(create_time__year=year,
                                  create_time__month=month).order_by('-create_time')
    return render(request, 'blog/blog.html', context={'post_list':post_list})



def categories(request,pk):

    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/blog.html', context={'post_list':post_list})


def tag(request,pk):
    tag=get_object_or_404(Tag,pk=pk)
    post_list=Post.objects.filter(tags=tag).order_by('-create_time')
    return render(request, 'blog/blog.html', context={'post_list':post_list})










