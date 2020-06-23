from django.contrib import admin
from .models import  Post,Category,Tag
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','create_time','modified_time','category','autho']
    fields = ['title','body','excerpt','category','tags']
    def save_model(self, request, obj, form, change):
        obj.autho=request.user
        super().save_model(request,obj,form,change)
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)