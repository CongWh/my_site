from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# 引入 Category 类
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView # 类视图
from pure_pagination.mixins import PaginationMixin 
from itertools import chain # 返回多个值用

class InitView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/base_pic.html'
    context_object_name = 'post_list' 
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 20


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list' 
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 20

class BaseView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/base.html'
    context_object_name = 'post_list' 
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 20	


class AboutView(BaseView):
    model = Post
    template_name = 'blog/about.html'
    context_object_name = 'post_list' 


	
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
 
    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
 
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
 
        # 视图必须返回一个 HttpResponse 对象
        return response
 
    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
 
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
 
        return post

'''		
# 点击侧边栏归档	
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
'''
	
class ArchiveView(IndexView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):   # 多参数在 kwargs 中
        year = self.kwargs['year']
        month = self.kwargs['month']
        return super().get_queryset().filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')

    def get_context_data(self, **kwargs):    # 传到html更多的上下文，即内容
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        context['archive_year'] = year;
        context['archive_month'] = month;
        return context										

		
		
	
# 点击侧边栏分类	
class CategoryView(IndexView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)



#def tag(request, pk):
#    # 记得在开始部分导入 Tag 类
#    paginate_by = 10
#    t = get_object_or_404(Tag, pk=pk)
#    post_list = Post.objects.filter(tags=t).order_by('-created_time')
#    return render(request, 'blog/index.html', context={'post_list': post_list})
class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))

        return super().get_queryset().filter(tags=t)	

    def get_context_data(self, **kwargs):    # 传到html更多的上下文，即内容
        context = super().get_context_data(**kwargs)
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        tag_name = t;
        context['tag_name'] = tag_name;
        return context
