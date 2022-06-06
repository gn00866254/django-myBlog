from pyexpat import model
from statistics import mode
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from matplotlib.image import thumbnail

class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=50)
    name_en = models.CharField('カテゴリ名英語', max_length=10)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self) -> str:
        return self.name


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False) #外部キー
    title = models.CharField('タイトル', max_length=50)
    content = models.TextField('内容', max_length=1000)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)#外部キー
    thumbnail = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)
    
    #管理画面に表示されるモデル内のデータ（レコード）を判別するための、名前（文字列）を定義することができます。
    def __str__(self) -> str:
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name='投稿', on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='Likeしたユーザー', on_delete=models.PROTECT)

      