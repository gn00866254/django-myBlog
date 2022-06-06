from audioop import reverse
from email import message
from re import template
from tempfile import tempdir
from unicodedata import category
from django.shortcuts import redirect, render,resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView,DeleteView,ListView
from .models import Post,Like,Category
from .forms import PostForm,LoginForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.author == self.request.user

class Index(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by("-created_at")
        context["post_list"]=post_list
        return context


class PostCreate(LoginRequiredMixin,CreateView):
    #テンプレート名はデフォルトで　モデル名_form.html　となる。
    model = Post
    form_class = PostForm
    # 投稿に成功した時のURL
    success_url = reverse_lazy('myapp:index')
    
    def form_valid(self, form) -> HttpResponse:
        form.instance.author_id = self.request.user.id
        return super(PostCreate,self).form_valid(form)

    # 投稿に成功した時に実行される処理
    def get_success_url(self):
        messages.success(self.request, '投稿が完了しました。')
        return super().get_success_url()


class PostDetail(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        detail_data=Post.objects.get(id = self.kwargs['pk'])
        #同じカテゴリのデータを取得
        category_posts=Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5]
        params = {
            'object':detail_data,
            'category_posts':category_posts,
        }
        return params
    

class PostUpdate(OnlyMyPostMixin,UpdateView):
    model = Post
    form_class=PostForm
    
    def get_success_url(self):
        messages.info(self.request,'Postを更新しました。')
        return resolve_url('myapp:post_detail',pk=self.kwargs['pk'])

class PostDelete(OnlyMyPostMixin,DeleteView):
    #デフォルトで確認画面作られている。モデル名_detail.html
    model = Post

    def get_success_url(self):
        messages.info(self.request, 'Postを削除しました。')
        return resolve_url('myapp:index')

class PostList(ListView):
    model = Post
    #並び順を定義
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Logout(LogoutView):
    template_name = 'myapp/logout.html'

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        self.object = user
        messages.info(self.request, 'ユーザー登録ができました。')
        return HttpResponseRedirect(self.get_success_url())


@login_required
def Like_add(request, post_id):
    post = Post.objects.get(id = post_id)
    is_liked = Like.objects.filter(user = request.user,post = post_id).count() #条件一致した投稿の数を取得
    if is_liked >0:
        messages.info(request, 'すでにお気に入りに追加済みです。')
        return redirect('myapp:post_detail', post.id)
    like = Like()
    like.user = request.user
    like.post = post
    like.save()

    messages.success(request, 'お気に入りに追加しました。')
    return redirect('myapp:post_detail', post.id)


class CategoryList(ListView):
    model = Category #自動的にcategory_listのページへ

class CategoryDetail(DetailView):
    model = Category
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'

    def get_context_data(self,*args, **kwargs):
        detail_data = Category.objects.get(name_en = self.kwargs['name_en'])
        category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')
        
        context = {
            'object':detail_data,
            'category_posts':category_posts,
        }
        
        return context
    
