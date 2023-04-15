from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Comment, Post, Category

admin.site.register(Post, MarkdownxModelAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)