from django.db import models
from posts.models import Post
# Create your models here.
class Comment(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    comment=models.CharField(max_length=4000)
    comment_image=models.ImageField(upload_to="comment_image",null=True,blank=True)
    comment_date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.comment
