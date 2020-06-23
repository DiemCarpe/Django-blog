from django.shortcuts import render
from django.http import HttpResponse
from .models import  Post
from django.shortcuts import  render,get_object_or_404
import markdown

def index(request):
    # return render(request,'blog/index.html',context={
    #     'title':'我的博客首页',
    #     'he':'hah'
    # })
    post_list=Post.objects.all().order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})


def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.body=markdown.markdown(post.body,
                                extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',
                                ])
    return render(request,'blog/detail.html',context={'post':post})



