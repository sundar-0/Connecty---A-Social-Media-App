from django.db import models
# Create your models here.
class FriendRequest(models.Model):
    request_from=models.ForeignKey('auth.User',on_delete=models.CASCADE,default=None,null=False,related_name='request_from')
    request_to=models.ForeignKey('auth.User',on_delete=models.CASCADE,default=None,null=False,related_name='request_to')
    status=models.CharField(max_length=50)






