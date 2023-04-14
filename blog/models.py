from django.db import models
import os #다운로드 파일 이름 알려줌

class Post(models.Model):
    title = models.CharField(max_length=30) #제목(글,길이30)
    content = models.TextField() #내용(글,무제한)
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True) #블로그 밑에 이미지/연월일까지 내려간 위치에서 저장/필수항목 아님
    file_upload= models.FileField(upload_to='blog/images/%Y/%m/%d/', blank=True) #업로드 필드

    created_at = models.DateTimeField(auto_now_add=True) #작성일시(자동수정)
    updated_at = models.DateTimeField(auto_now=True) #시간 자동 업뎃
    
    def __str__(self):
        return f'[{self.pk}]{self.title}' #pk=번호, 제목

    def get_absolute_url(self):
        return f'/blog/{self.pk}/' #글 상페 url 설정
        
    def get_file_name(self):
        return os.path.basename(self.file_upload.name) #다운로드 파일 이름 나타냄

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #다운로드 확장자 나타냄