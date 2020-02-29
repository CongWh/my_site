

# Create your tests here.
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
 
app_name = 'blog'  ## 命名空间
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('', views.InitView.as_view(), name='init'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'), # 跳转到文章详情
 #   path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
	path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
	
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    #path('tags/<int:pk>/', views.tag, name='tag'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
	
	path('about', views.AboutView.as_view(), name='about'),
	
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)