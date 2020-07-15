from rest_framework import serializers
from .models import Profile, Product, Location, Category, Subcategory, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import base64
from drf_extra_fields.fields import Base64ImageField
from rest_framework.authtoken.models import Token

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['bio','phone','photo']

class UserSerializer(serializers.ModelSerializer):
    
    profile = UserProfileSerializer() 
    class Meta:
        model = User
        
        fields = ['id','username','email','first_name','last_name','profile','is_staff','is_active','date_joined','is_superuser']

class ProfileSeializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:

        model = Location
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name']

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance

class SubcategorySerializer(serializers.ModelSerializer):
    
    category = CategorySerializer()
    class Meta:
        model = Subcategory
        fields = ['id','name','category']
    
    def create(self, validated_data):
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
   
    # location = LocationSerializer()
    # category = SubcategorySerializer()
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'image', 'price', 'created_at','updated', 'location','category']

    def update(self, instance, validated_data):
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.price = validated_data.get('price', instance.price)
        instance.location_id = validated_data.get('location', instance.location_id)
        instance.category_id = validated_data.get('category', instance.category_id)
        instance.updated = timezone.now()
        instance.save()
        return instance
    
    def create(self, validated_data,user):
        
        title = validated_data.get('title')
        description = validated_data.get('description')
        image = validated_data.get('image')
        price = validated_data.get('price')
        location = validated_data.get('location')
        category = validated_data.get('category')
        slug = validated_data.get('slug')
        created_at = timezone.now()
        
        product = Product.objects.create(
            user = user,
            title = title,
            description = description,
            image = image,
            price = price,
            location = Location.objects.get(id = location),
            category = Subcategory.objects.get(id = category),
            created_at = created_at,
            slug = slug
        )

        return product

    
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    phone = serializers.CharField()

    class Meta:
        model = get_user_model()        
        fields = ['username','email','phone','first_name','last_name','password']

    def create(self, validate_data):
        try:
            user = get_user_model().objects.create(
                username = validate_data['username'],
                email = validate_data['email'],
                first_name = validate_data['first_name'],
                last_name = validate_data['last_name'],
                password = validate_data['password'],
                
            )
        except ObjectDoesNotExist:
            raise {"status" : "failed", "error" : "Can not create user"}

        profile = Profile.objects.create(
            user = user,
            phone = validate_data['phone']
        )

        return [user, profile]

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username','password']
    
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self,pk,validated_data):
        user = Token.objects.get(key=validated_data['token']).user
        Comment.objects.create(user = user, 
                               comment = validated_data['comment'],
                                product_id = pk,
                                post_date = timezone.now())
      
        
            

