from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-pk' #최근 목록순으로 보기


class PostDetail(DetailView):
    model = Post    
# Create your views here.
