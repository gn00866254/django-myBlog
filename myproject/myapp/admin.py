from unicodedata import category
from django.contrib import admin
from .models import Post,Like,Category


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title','thumbnail','created_at')
    list_display_links = ('title',)
    ordering = ('-created_at', )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id','user','post')
    list_display_links = ('post',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('name',)