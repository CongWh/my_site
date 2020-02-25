

# Create your tests here.
from django.urls import path
 
from . import views
 
app_name = 'blog'  ## 命名空间
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('', views.InitView.as_view(), name='init'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'), # 跳转到文章详情
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    #path('tags/<int:pk>/', views.tag, name='tag'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
]