from django.contrib import admin
from django.contrib import admin
from WearWellWardrobe.models import Category, Page

admin.site.register(Category)
admin.site.register(Page)



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


