from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import http.client
import json
import uuid




class Category(models.Model):
    name = models.CharField(max_length=128)
    ID = models.AutoField(primary_key=True, unique=True)
    
    # if redoing teh DB, add extra potentiul colour feild for each categroy
    #colour = models. ---- something here.....
    
    
    def __str__(self):
        return self.name
        
 
  # The admin Side of it adds 's' to the end of the string. 
  #Here is allows you to change the plural of it
    class Meta:
        verbose_name_plural = 'Categories'
        

        
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    page_id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=128,default="Untitled",null=True, blank=True)
    content1 = models.CharField(max_length=8000,default="",null=True, blank=True) # change length?
    content2 = models.CharField(max_length=8000,default="",null=True, blank=True) 
    content3 = models.CharField(max_length=8000,default="",null=True, blank=True) 
    content4 = models.CharField(max_length=8000,default="",null=True, blank=True) 
    img1 = models.ImageField(upload_to="contentPhotos/",default="",null=True, blank=True)
    
    displayStyle = models.IntegerField(default=1)   # for react to know which page to make the content display in.
                                                    # 0 is probably for those that are part of the flow chartss
    slug = models.SlugField(default="",unique=True,null=True, blank=True)
    pageNotes = models.CharField(max_length=4096,default="",null=True, blank=True) # a field to allow notes to display on editing page, 
            #such as this page is for a flow char or where this page is acessable from 
    deletable =  models.BooleanField(default=True) # Possible issue - false means it can be deleted, due to an unknown issue when automatically puting this field in.
    
    # for question feilds, title = Question, and content1->4 are the options text/data
        # probably depends on how we want to alter th pages later..
        # image1 also availbe if we want an image to go with the text
        
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        

        unique_slug = self.slug
        num = 1
        while Page.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{self.slug}-{num}"
            num += 1

        self.slug = unique_slug
        super(Page, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True, null=True, default="")

    def __str__(self):
        return self.user.username
        
        
        
        
        
        