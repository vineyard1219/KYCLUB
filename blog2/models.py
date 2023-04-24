from django.db import models
from django.contrib.auth.models import User #유저 추가
from markdownx.models import MarkdownxField #마크다운 적용
from markdownx.utils import markdown #마크다운 문법적용
import os

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog2/category/{self.slug}/'    

    class Meta:
        verbose_name_plural = "Categories"

class Post(models.Model):
    title = models.CharField(max_length=30) #제목(글,길이30)
    hook_text = models.CharField(max_length=100, blank=True) #요약문필드
    content = MarkdownxField() #내용(글,무제한)
    
    head_image = models.ImageField(upload_to='blog2/images/%Y/%m/%d/', blank=True) #블로그 밑에 이미지/연월일까지 내려간 위치에서 저장/필수항목 아님
    file_upload= models.FileField(upload_to='blog2/images/%Y/%m/%d/', blank=True) #업로드 필드

    created_at = models.DateTimeField(auto_now_add=True) #작성일시(자동수정)
    updated_at = models.DateTimeField(auto_now=True) #시간 자동 업뎃
    
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='blog2_posts') #작성자정보 담름(?) 외래키

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='blog2_posts') #카테고리
    
    
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}' #pk=번호, 제목 :: 외래키

    def get_absolute_url(self):
        return f'/blog2/{self.pk}/' #글 상페 url 설정
        
    def get_file_name(self):
        return os.path.basename(self.file_upload.name) #다운로드 파일 이름 나타냄

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #다운로드 확장자 나타냄
    
    def get_content_markdown(self):
        return markdown(self.content)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f'{self.author}::{self.content}'
    
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1503/fd7b91377dd76b87/svg/{ self.author.username }.png'