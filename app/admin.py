from django.contrib import admin
from .models import (Product, Profile,
                    Like, Dislike, 
                    Location, Comment, 
                    Subcategory, Category
                )

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category'
    ]

class CommmentAdmin(admin.ModelAdmin):
    
    list_display = [
        'user',
        'product',
        'post_date'
    ]

    search_fields = [
		'user__username',
		
	]

    list_filter = [
        'post_date',
        'product'
    ]
class LikeAdmin(admin.ModelAdmin):

    list_display = [
      
        'product',
        'created_time'

    ]
class DislikeAdmin(admin.ModelAdmin):

    list_display = [
      
        'product',
        'created_time'

    ]

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Dislike,DislikeAdmin)
admin.site.register(Location)
admin.site.register(Comment,CommmentAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(Subcategory,SubcategoryAdmin)
admin.site.register(Category,CategoryAdmin)