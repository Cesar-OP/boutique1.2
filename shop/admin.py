from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['thumbnail','name', 'slug', 'price',
                    'available', 'created', 'updated','stock']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available','stock']
    prepopulated_fields = {'slug': ('name',)}
   

    def thumbnail(self, obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.image.url))
    

    


    thumbnail.allow_tags = True
    thumbnail.short_description = "Thumbnail"
    
    def save_model(self,request, obj, form, change):
        if obj.stock == 0:
            obj.available = False
        elif obj.stock > 0 :
            obj.available = True
        
        super().save_model(request, obj, form, change)
        
