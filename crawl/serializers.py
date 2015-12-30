from django.contrib.auth import get_user_model
from rest_framework import serializers

from crawl.models import News, UserToken


class NewsSerializer(serializers.ModelSerializer):
    
    class Meta:
      model = News
      fields = ('id','news_url','title','source','upvote','comment')

class UserDetailSerializer(serializers.ModelSerializer):
    user_token =  serializers.SerializerMethodField('get_token')

    class Meta:
        model = get_user_model()
        fields = ('id','username','email','date_joined','first_name','last_name','user_token')

    def get_token(self, container):
        user_requested = self.context['request'].user
        token_obj = UserToken.objects.get(user=user_requested)
        return_data = {}
        return_data['token'] = token_obj.token
        return return_data