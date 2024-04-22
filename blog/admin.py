from django.contrib import admin
from .models import BlogCategory, Blog, BlogComment


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'pub_time', 'category', 'author']


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'pub_time', 'author', 'blog']


admin.site.register(BlogCategory, BlogCategoryAdmin)   # first model，在管理BlogCategory时用的是BlogCategoryAdmin
admin.site.register(Blog, BlogAdmin)                  # 2nd model
admin.site.register(BlogComment, BlogCommentAdmin)   # 3rd model