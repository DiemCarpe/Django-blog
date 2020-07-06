from django.apps import AppConfig

#让 blog 应用在 django 的 admin 后台显示中文名字
class CommentsConfig(AppConfig):
    name = 'comments'
    verbose_name='评论'