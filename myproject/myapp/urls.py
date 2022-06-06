from django.urls import path, include
from . import views

app_name = "myapp"

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('post_create', views.PostCreate.as_view(), name='post_create'),
    #int:整数値、pkはDjangoに備わった照合形式で、主キー（PRIMARY KEY）を表します。
    path('post_detail/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('post_update/<int:pk>', views.PostUpdate.as_view(), name='post_update'), 
    path('post_delete/<int:pk>', views.PostDelete.as_view(), name='post_delete'),
    #投稿一覧
    path('post_list', views.PostList.as_view(), name='post_list'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('like/<int:post_id>', views.Like_add, name='like_add'),
    path('category_list', views.CategoryList.as_view(), name='category_list'),
    path('category_detail/<str:name_en>', views.CategoryDetail.as_view(), name='category_detail'),
]