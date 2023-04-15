from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin #로그인할때만 정상 페이지
from .models import Post, Category
from django.core.exceptions import PermissionDenied #글작성자만 수정가능


class PostList(ListView):
    model = Post
    ordering = '-pk' #최근 목록순으로 보기
    
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
            
        return context
    

class PostDetail(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        
        return context


class PostCreate(LoginRequiredMixin, CreateView): #글작성 폼
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user #웹사이트 방문자
        if current_user.is_authenticated: #로그인 유무 확인
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
                return redirect('/blog/')



class PostUpdate(LoginRequiredMixin, UpdateView): #글수정
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    
    template_name = 'blog/post_update_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    



def category_page(request, slug): #카테고리
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        
        }
    )
    
        
# Create your views here.
