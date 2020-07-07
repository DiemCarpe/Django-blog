from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from django.utils.html import strip_tags
import markdown



class Category(models.Model):
    """
    django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='分类'
        verbose_name_plural=verbose_name
class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='标签'
        verbose_name_plural=verbose_name
class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """
    #文章标题
    title=models.CharField('标题',max_length=70)
    #文章内容
    body=models.TextField('正文')
    #文章创建时间与最后一次修改时间
    create_time=models.DateTimeField('创建时间',default=timezone.now)
    modified_time=models.DateTimeField('修改时间')
    #摘要
    excerpt=models.CharField('摘要',max_length=150,blank=True)
    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一
    # 对多的关联关系。且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    category=models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag,verbose_name='标签',blank=True)
    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和
    # Category 类似。
    autho=models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    class Meta:
        """
        django 允许我们在 models.Model 的子类里定义一个名为 Meta 的内部类，
        通过这个内部类指定一些属性的值来规定这个模型类该有的一些特性，
        例如在这里我们要指定 Post 的排序方式。
        首先看到 Post 的代码，在 Post 模型的内部定义的 Meta 类中，指定排序属性 ordering：
        ordering 属性用来指定文章排序方式，['-created_time'] 指定了依据哪个属性的值进行排序，
        这里指定为按照文章发布时间排序，且负号表示逆序排列。
        列表中可以有多个项，比如 ordering = ['-created_time', 'title']
        表示首先依据 created_time 排序，如果 created_time 相同，则再依据 title 排序。
        这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序，
        因此可以删掉视图函数中对文章列表中返回结果进行排序的代码了。


        """
        verbose_name='文章'
        verbose_name_plural=verbose_name

        ordering=['-create_time']

    def __str__(self):
        return self.title



    #在model被save到数据库前，指定modified_time的值为当前时间
    def save(self,*args,**kwargs):
        self.modified_time=timezone.now()
        """
        
        首先实例化一个 Markdown 类，用于渲染 body 的文本
        由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md=markdown.Markdown(extensions=[
             'markdown.extensions.extra',
            'markdown.extensions.codehilite',
         ])
         先将 Markdown 文本渲染成 HTML 文本
         strip_tags 去掉 HTML 文本的全部 HTML 标签
         从文本摘取前 54 个字符赋给 excerpt
         self.excerpt=strip_tags(md.convert(self.body))[:54]
         
        """
        #直接去掉HTML文本
        self.excerpt=strip_tags(self.body)[:54]
        super().save(*args,**kwargs)

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})




class Weather(models.Model):
    """
    天气
    """
    pass