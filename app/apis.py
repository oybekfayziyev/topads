from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import (ProfileSeializer, 
                        ProductSerializer, 
                        RegisterSerializer, 
                        UserSerializer,
                        CategorySerializer,
                        SubcategorySerializer,
                        CommentSerializer
                    )
from .models import (Profile, Product, 
                    Category, Subcategory, 
                    Comment, Like, Dislike)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError
from .models import CATEGORY_CHOICES
# REST FRAMEWORK
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action


'''
Include Admin users Token in the Header
'''
class UserApi(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    
    def get(self,request):
      
        users = UserSerializer(instance = User.objects.all(), many = True)
        return Response(users.data, status=status.HTTP_200_OK)
'''
Params:
    username
    email = blank is True
    first_name
    last_name
    phone = blank is True
    password
'''
class LogoutApi(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            Response(status=status.HTTP_400_BAD_REQUEST)
        django_logout(request)
        return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)

class RegisterApi(APIView):

    def post(self,request):
        try:
            username = request.data['username']
            email, phone = '', ''
            
            if request.data['email']:
                email = request.data['email']
            elif request.data['phone']:
                phone = request.data['phone']            
            password1 = request.data['password']
            
            name = request.data['first_name']
            surname = request.data['last_name']
        except ObjectDoesNotExist:
            return JsonResponse({"status" : "failed","error" : "Some of the attributes are missing"})
        
        try:
            user = User.objects.create_user(
                username = username,
                email = email,
                password = password1,            
                first_name = name,
                last_name = surname
            )
        except:
            return JsonResponse({"status" : "failed", "Error" : "Username is already exist"})
                  
        profile = Profile.objects.create(user = user,phone = phone)
        token,created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            "username" : user.username,
            "email" : email,
            "name" : name,
            "surname" : surname,
            "token" : token.key
        })
    
        return JsonResponse({"status" : 'failed', 'error' : 'Can not create user'})

# @action(detail=False, methods=['post'])
# def logout(self, request):
#     try:
#         request.user.auth_token.delete()
#     except (AttributeError, ObjectDoesNotExist):
#         pass

#     django_logout(request)
#     return Response(status=status.HTTP_200_OK)

class ProductApi(viewsets.ViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]      
    authentication_classes = [TokenAuthentication]

    def list(self,request):
        product = ProductSerializer(instance=Product.objects.all(), many = True)
      
        return Response(product.data)
        
    def create(self,request,slug=None):       
        try:
            user = Token.objects.get(key = request.data['token']).user
        except ObjectDoesNotExist:
            return Response(data = {"status" : "failed", "error" : "User is not found"}, status = status.HTTP_401_UNAUTHORIZED)

        try:            
            ProductSerializer(instance = Product.objects.get(user=user, slug=slug))
            return Response(data={"status": "failed","error" : "Product is already exists with this slug"},status = status.HTTP_403_FORBIDDEN)
            
        except ObjectDoesNotExist:  
            product = ProductSerializer(instance = Product.objects.filter(user=user),data=request.data)
            product.is_valid(raise_exception=True)
            product.create(request.data,user)       
            return Response(data = {"status" : "success",'message' : 'Product is created'},status = status.HTTP_202_ACCEPTED)
            
        except IntegrityError:
            return Response(data = {'status' : 'failed','error' : 'Slug is already defined'},status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,slug=None):
        try:
            product = ProductSerializer(instance = Product.objects.get(slug = slug))
            return Response(product.data)
        except ObjectDoesNotExist:
            return Response({"status" : "failed", "error" : "Product with this slug is not found"},status=status.HTTP_400_BAD_REQUEST)

    '''
    Params:
        token of the User
        title,
        description
        image
        price
        location_id
        category_id
    '''
    def update(self,request,slug = None):
        
        try:
            user = Token.objects.get(key = request.data['token']).user
        except ObjectDoesNotExist:
            return Response(data = {"status" : "failed", "error" : "User is not found"}, status = status.HTTP_401_UNAUTHORIZED)
       
        try:
            product = ProductSerializer(instance=Product.objects.get(user = user, slug = slug),data=request.data)                 
            product.is_valid(raise_exception=True)
            product.update(Product.objects.get(user=user,slug=slug),request.data)
            
           
            return Response(status = status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response(data={"status": "failed","error" : "This user has not an item with this slug"},status = status.HTTP_403_FORBIDDEN)

class GetCategoryApi(viewsets.ViewSet):


    def list(self,request):
        try:             
            category = CategorySerializer(instance=Category.objects.all(),many=True)             
            return Response(category.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'status':'failed','error':'Object is not found'},status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
                
        try:
            category = CategorySerializer(instance=Category.objects.get(id=pk),many=False)
            return Response(category.data,status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'status':'failed','message':'Category id is not found'},status=status.HTTP_400_BAD_REQUEST)



class CategoryApi(viewsets.ViewSet):   

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    def update(self,request,pk):       
        try:
            category = CategorySerializer(instance=Category.objects.get(id=pk),data=request.data)
            category.is_valid(raise_exception=True)
            category.update(Category.objects.get(id=pk),request.data)
            return Response({'status':'success','message':'Category successfully updated'},status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({'status':'failed','message':'Category id is not found'},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
        try:
            category = CategorySerializer(data=request.data)
            category.is_valid(raise_exception=True)
            category.save()
            return Response({'status':'success','message':'Category created successfully'},status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({'status':'failed','message':'Category id is not found'},status=status.HTTP_400_BAD_REQUEST)

    
class GetSubcategoryApi(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
  
class SubcategoryApi(viewsets.ViewSet):
    
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def update(self,request,pk=None):
        try:           
            if not request.data.get('category'):
                return Response({'status':'failed','message':'Category is required'},status=status.HTTP_400_BAD_REQUEST)
            
            if not request.data.get('name'):
                return Response({'status':'failed','message':'Name is required'},status=status.HTTP_400_BAD_REQUEST)

            category = Subcategory.objects.get(id=pk).category              
            get_choice = [cat for cat in CATEGORY_CHOICES if request.data['category'] in cat]
            if not get_choice:
                return Response({'status':'failed','message':'%s is not in category choices' %request.data['category']},status=status.HTTP_400_BAD_REQUEST)
                                    
            category.name = request.data['category']            
            category.save()

            subcategory = Subcategory.objects.get(id=pk)
            subcategory.category = category
            subcategory.name = request.data['name']
            subcategory.save()

            return Response({'status':'success','message':'Subcategory successfully updated'},status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status':'failed','message':'Subcategory is not found with this id'},status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        try:
            category = Category.objects.all()

            if not category:
                category = Category.objects.create(name = request.data['category'])

            if not ([cats for cats in CATEGORY_CHOICES if request.data['category'] in cats]):
                return Response({'status':'failed','message':'%s is not in category choices' % request.data['category']},status=status.HTTP_400_BAD_REQUEST)
            
            if not request.data['category'] == [cats.name for cats in category if request.data['category'] in cats.name][0]:
                category = Category.objects.create(name = request.data['category'])           
            
            else:
                category = Category.objects.get(name=request.data['category'])
                
            print('category',category)
            Subcategory.objects.create(
                name = request.data['name'],
                category = category
            )
                
            return Response({'status':'success','message':'Category created successfully'},status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({'status':'failed','message':'Category id is not found'},status=status.HTTP_400_BAD_REQUEST)

class CommentApi(viewsets.ViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self,request,pk):

        try:
            comment = CommentSerializer(instance = Comment.objects.filter(product_id=pk),many=True)
            
            return Response(comment.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'data':'Commend pk is not found'},status=status.HTTP_400_BAD_REQUEST)

    def create(self,request,pk):

        try:
            user = Token.objects.get(key = request.data['token']).user
        except ObjectDoesNotExist:
            return Response(data = {"status" : "failed", "error" : "User is not found"}, status = status.HTTP_401_UNAUTHORIZED)

        try:            
            comment = CommentSerializer(instance = Comment.objects.filter(user=user, product_id=pk),data=request.data)
          
            comment.is_valid()
            comment.create(pk,request.data)

            return Response({"detail":"Successfully commented"},status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            return Response({'data':'Comment does not exist'},status=status.HTTP_400_BAD_REQUEST)
    
    def drop(self,request,p_id,c_id):
        try:
            user = Token.objects.get(key=request.data['token']).user

        except ObjectDoesNotExist:
            return Response(data = {"status" : "failed", "error" : "User is not found"}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            comment =  Comment.objects.get(product__user = user, product_id = p_id, id=c_id)            
            comment.delete()

            return Response(data = {'status':'success','message':'Comment deleted successfully'},status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            try:
                comment = Comment.objects.get(user_id = user, product_id = p_id, id = c_id)
                comment.delete()

                return Response(data = {'status':'success','message':'Comment deleted successfully'},status=status.HTTP_200_OK)
            
            except ObjectDoesNotExist:                
                return Response({'detail':'You dont have permission to delete this comment'},status=status.HTTP_400_BAD_REQUEST)

class LikeApi(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self,request,pk):        
        user = self.request.user     
        like_obj, created = Like.objects.get_or_create(product_id = pk)
        updated = False
        liked = False

        if user in like_obj.user.all():
            like_obj.user.remove(user)
        else:
            like_obj.user.add(user)
            liked = True
        updated = True
        like_obj.save()
                
        return Response({'updated' : updated, 'liked' : liked},status=status.HTTP_201_CREATED)
        
class DislikeApi(viewsets.ViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self,request,pk):        
        dislike_obj, created = Dislike.objects.get_or_create(product_id = pk)
        user = self.request.user
        updated = False
        liked = False
        if user in dislike_obj.user.all():
            dislike_obj.user.remove(user)
        else:
            dislike_obj.user.add(user)
            liked = True
        updated = True
        dislike_obj.save()
                
        return Response({'updated':updated,'liked':liked},status=status.HTTP_201_CREATED)

class ProfileApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            profile = ProfileSeializer(instance=Profile.objects.all())
            return Response(profile.data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail':'Object does not exist'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk):
        pass

    def post(self,request):
        pass
