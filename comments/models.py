from django.db import models
from django.utils import timezone


class Comment(models.Model):
    """
    评论是关联到某篇文章（Post）的
    由于一个评论只能属于一篇文章
    一篇文章可以有多个评论，是一对多的关系，因此这里我们使用了 ForeignKey
    """
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    text = models.TextField('评论内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        #根据创建时间排序
        ordering= ['-created_time']

    def __str__(self):
        return '{}:{}'.format(self.name, self.text[:20])
