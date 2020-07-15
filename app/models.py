from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
CITY_CHOICES = (
    ('A', 'Andijon'),
    ('B', 'Buxoro'),
    ('F', 'Fargona'),
    ('J', 'Jizzax'),
    ('X', 'Xorazm'),
    ('N', 'Namangan'),    
    ('N', 'Navoi'),
    ('Q', 'Qashqadaryo'),
    ('QQ', "Qoraqalpog'iston Respublikasi"),
    ('S', 'Samarqand'),
    ('SD', 'Sirdaryo'),
    ('SU', 'Surxondaryo'),
    ('T', 'Toshkent')
)

CATEGORY_CHOICES = (
    ('V', 'Vehicles'),
    ('P', 'Property'),
    ('ES', 'Electronics'),
    ('KFHB', 'Kids, Fashion, Health & Beauty'),
    ('ETS', 'Essentials'),
    ('HG', 'Home & Garden'),
    ('HS', 'Hobby & Sports'),
    ('S', "Services"),
    ('E', 'Education'),
    ('BI', 'Business & Industry'),
    ('FA', 'Food & Agriculture'),
    ('O', 'Other'),

)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)    
    photo = models.ImageField(upload_to='images/profile/', blank=True,null=True)
    bio = models.CharField(max_length=400,blank=True,null=True)
    phone = models.CharField(max_length=15, blank=True,null=True)
    def __str__(self):
        return self.user.username

    

class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length = 512)
    image = models.ImageField('images/products/{id}/')
    price = models.FloatField(blank = True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True,max_length=500)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    category = models.ForeignKey('Subcategory', on_delete=models.CASCADE, blank=True,null=True)
    def __str__(self):
        return self.title    
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super(Product, self).save(*args, **kwargs)

class Like(models.Model):
    user = models.ManyToManyField(User, related_name='like')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True, blank=True,null=True)

    def __str__(self):
        return f'Liked {self.product.title}'

    def total_likes(self):
        return self.like.user.count()

    
class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name='dislike')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    dislike = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    
    def __str__(self):
        return f'Disliked {self.product.title}'
    
    def total_dislikes(self):
        return self.dislike.user.count()

class Category(models.Model):
    name = models.CharField(max_length = 5, choices = CATEGORY_CHOICES, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    name = models.CharField(max_length = 50)

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f'{self.name} of {self.category.name}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.title} commented by {self.user.username}'


class Location(models.Model):
    address = models.CharField(max_length = 50)
    city = models.CharField(max_length = 2, choices = CITY_CHOICES)
    district = models.CharField(max_length = 50)

    def __str__(self):
        return self.address

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

