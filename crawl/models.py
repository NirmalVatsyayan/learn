from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
   
    news_url = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    source = models.CharField(max_length = 200)
    upvote = models.CharField(max_length = 200)
    comment = models.CharField(max_length = 200)
    
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    
    def __str__(self):
        return "News ID {}".format(self.id)

class UserToken(models.Model):

    user = models.ForeignKey(User,related_name="token_user")
    token = models.CharField(max_length=500)

    def __str__(self):
        return "UserToken ID {}".format(self.id)

class UserDeletedNews(models.Model):

    user = models.ForeignKey(User,related_name="delete_news_user")
    news = models.ManyToManyField(News,related_name="news_deleted")

    def __str__(self):
        return "UserDeletedNews ID {}".format(self.id)
