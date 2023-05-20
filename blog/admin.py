from django.contrib import admin
from .models import Blogger, Blog, Comment


admin.site.register(Comment)


class BloggerInline(admin.TabularInline):
    model = Blog


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')

    fields = ['name', 'bio']

    inlines = [BloggerInline]


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


