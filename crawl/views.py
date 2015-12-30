from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.generics import GenericAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework_jwt.settings import api_settings as jwt_settings
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from crawl.serializers import NewsSerializer, UserDetailSerializer
from crawl.models import News, UserToken, UserDeletedNews
# Create your views here.

jwt_payload_handler = jwt_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = jwt_settings.JWT_DECODE_HANDLER

def getUserToken(user):
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)

class IsPermitted(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == None:
            return False
        else:
            try:
                token_map = UserToken.objects.get(token=token)
                request.user = token_map.user
                return token_map.user
            except:
                return False

class DispatcherView(APIView):
    """
       HTTP_AUTHFLAG:Authorization -- "login <login>"
    """
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'GET', 'PATCH',)

    def post(self, request, *args, **kwargs):
        if request.META.__contains__('HTTP_AUTHFLAG'):
            authflag = request.META['HTTP_AUTHFLAG']
            if authflag == 'login':
                return UserLoginView.as_view()(request._request)
            if authflag == 'logout':
                return Logout.as_view()(request._request)    
            elif authflag == 'register':
                return UserView.as_view()(request._request)
            else:
                return Response({"ERROR":'please give one of login, register, logout'}, status=status.HTTP_400_BAD_REQUEST)            
        else:
            return Response({"ERROR":'please give either one of authflag http header'}, status=status.HTTP_400_BAD_REQUEST)                

    def get(self, request, *args, **kwargs):
        return Response({"ERROR":'method GET not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        return Response({"ERROR":'method PATCH not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        return Response({"ERROR":'method PUT not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)             

    def delete(self, request, *args, **kwargs):
        return Response({"ERROR":'method DELETE not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)    



class UserView(APIView):

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({API_ERROR:'method GET not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({API_ERROR:'method PUT not_allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        return UserDetailSerializer    

    def post(self, request, *args, **kwargs):
        username = self.request.data.get('username')
        full_name = self.request.data.get('name')
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        
        absent_fields = {}
        absent_message = "Not present"

        if username == None or username == '':
            absent_fields['username'] = absent_message
        if full_name == None or full_name == '':
            absent_fields['name'] = absent_message
        if email ==  None or email == '':
            absent_fields['email'] = absent_message
        if password == None or password == '':
            absent_fields['password'] = absent_message

        if len(absent_fields):
            return Response({"ERROR":absent_fields}, status=status.HTTP_400_BAD_REQUEST)    
        

        email = email.strip()
        password = password.strip()
        full_name = full_name.split(" ")

        first_name = full_name[0].strip()
        last_name = ''
        for i in range(1,len(full_name)):
        	last_name = last_name+full_name[i] + " "
        
        already_exist = User.objects.filter(email=email)
        already_existusernme = User.objects.filter(username__iexact=username.strip())
        if bool(already_exist):
            raise ValidationError(detail={"ERROR":"This email is already registered"})
        elif bool(already_existusernme):
        	raise ValidationError(detail={"ERROR":"This username is already taken"})
        else:
            #password = make_password(password)
            new_user = User(username=username,first_name=first_name, last_name=last_name,password=password, email=email)
            new_user.save()
            token = getUserToken(new_user)
            user_token = UserToken.objects.create(user=new_user,token=token)
            self.request.user = new_user
            context = {'request':self.request}
            user_data = UserDetailSerializer(new_user,context=context)
            return Response(user_data.data, status=status.HTTP_200_OK)    
           
        
    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 100
        return 10       

class UserLoginView(APIView):

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({API_ERROR:'method GET not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({API_ERROR:'method PUT not_allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        return UserDetailSerializer    

    def post(self, request, *args, **kwargs):
        email = self.request.data.get('Email')
        password = self.request.data.get('Password')
        
        absent_fields = {}
        absent_message = "Not present"

        if email == None or email == '':
            absent_fields['email'] = absent_message
        if password == None or password == '':
            absent_fields['password'] = absent_message

        if len(absent_fields):
            return Response({"ERROR":absent_fields}, status=status.HTTP_400_BAD_REQUEST)    
        

        email = email.strip()
        password = password.strip()
        
        
        try:
            user = User.objects.get(email=email,password=password)
        except:
            raise ValidationError(detail={"ERROR":"Invalid Login credential"})
        
        
        token = getUserToken(user)
        user_token = UserToken.objects.filter(user=user)
        for val in user_token:
            val.delete()
        user_token = UserToken.objects.create(user=user,token=token)
        self.request.user = user
        context = {'request':self.request}
        user_data = UserDetailSerializer(user,context=context)
        return Response(user_data.data, status=status.HTTP_200_OK)    
           
        
    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 100
        return 10     

class NewsGet(ListAPIView):

    permission_classes = (IsPermitted,)

    def get_serializer_class(self):
        return NewsSerializer

    def get_queryset(self):
        try:
            news_delete = UserDeletedNews.objects.get(user=self.request.user)
            delete_news = news_delete.news.all()
            delete_news_id = [o.id for o in delete_news]
            news = News.objects.all().exclude(id__in=delete_news_id).order_by('-updated')        
        except:
            news = News.objects.all().order_by('-updated')
        return news


@api_view(['PATCH',])
@permission_classes([IsPermitted,])
def DeleteNews(request):
    news_id = request.query_params['news_id']
    
    user = request.user
    news_delete , created = UserDeletedNews.objects.get_or_create(user=user)
    
    news_obj = News.objects.get(id=news_id)
    news_delete.news.add(news_obj)
    return Response({"SUCCESS":"OK"}, status=status.HTTP_200_OK)    