from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
)
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from WearWellWardrobe import views
## Added Stuff for API`s
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from other pages
from WearWellWardrobe.models import Category, Page
from WearWellWardrobe.serializers import ItemSerializer
from WearWellWardrobe.forms import PageForm, EditPageForm, EditCategoryForm



def index(request):
    return render(request, "home.html")


# log in required for the rest of these -> once its set up

# the main page -> basically wants everything

def home(request):
    context_dict = {}
    try:
        pages = Page.objects.all()
        cats = Category.objects.all()
        context_dict['pages'] = pages
        context_dict['category'] = cats
    
    except:
        pass

    return render(request, "loggedInHome.html", context=context_dict)


def viewPage(request, pageSlug):
# code that view the page -> can probably be deleted 
    context = {}
    try:
        pageData = Page.objects.get(slug=pageSlug)
        context["page"] = pageData
    except Page.DoesNotExist:
        context["page"] = None
    #  can insert stuff about redirecting here
    return render(request, "", context=context)

# editPage view -> redirect back to home page once done
def editPage(request, pageSlug):
    
    context = {}
    try:
        pageData = Page.objects.get(slug=pageSlug)
    except Page.DoesNotExist:
        context["page"] = None
        return redirect("WearWellWardrobe:home") 
    
    if request.method =="POST":
        form = EditPageForm(request.POST, request.FILES, instance=pageData)
        if form.is_valid():
            form.save(commit=True)
            return redirect("WearWellWardrobe:home")
        else:
            print(form.errors)
            
            
    else:
        context["page"] = pageData
        initial = {
            'title': pageData.title,
            'content1': pageData.content1,
            'content2': pageData.content2,
            'content3': pageData.content3,
            'content4': pageData.content4,
            'img1': pageData.img1,
            'pageNotes': pageData.pageNotes,
            'category': pageData.category,
        }
        form = EditPageForm(initial=initial, instance=pageData)     
        return render(request, "itemPage.html", {'form': form, "page":pageData})

        

# addPage page (deals with both form input and link to page) 
# redirects back to home page once completed
def addPage(request):
    form = PageForm(request.POST, request.FILES)
    
    if form.is_valid():
        form.save(commit=True)
        return redirect("WearWellWardrobe:home")
    else:
        print(form.errors)
        # return some usefull error messages to the page?
   
    context_dict = {'form': form}
    return render(request, 'addPage.html', context=context_dict)
    
    
def doneCategory(request):
    return render(request, "categroyDone.html")

def editCategory(request, catSlug):
    context = {}
    try:
        catData = Category.objects.get(ID=catSlug)
    except Category.DoesNotExist:
        context["category"] = None
        return redirect("WearWellWardrobe:doneCategory") 
    
    if request.method =="POST":
        form = EditCategoryForm(request.POST, instance=catData)
        if form.is_valid():
            form.save(commit=True)
            return redirect("WearWellWardrobe:doneCategory")
        else:
            print(form.errors)
            
            
    else:
        context["page"] = catData
        initial = {
            'name': catData.name,
            
        }
        form = EditCategoryForm(initial=initial, instance=catData)     
        return render(request, "categoryeditPage.html", {'form': form, "category":catData})        
        
        
        
        
# delete request?
def deletePage(request, pageSlug):
    pageData = Page.objects.get(slug=pageSlug)

    if request.method == "POST":
        pageData.delete()
        return redirect("WearWellWardrobe:home") 

    return render(request, "delete.html", {"page": pageData})
   
class PageGet(APIView):
    def get(self, request):
        pages = Page.objects.all()
        serializer = ItemSerializer(pages, many=True)
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = '*'  
        return response
        
    # below is code that could allow data sent into the DB, but ive commented it out
    #    to disable it for now
    
    #def post(self, request):
    #    serializer = ItemSerializer(data=request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RecordDetail(APIView):
    def get(self, request, pk, format=None):
        # Fetch the record by primary key (pk)
        item = get_object_or_404(Item, pk=pk)
        
        # Serialize the item and return as JSON
        serializer = ItemSerializer(item)
        return Response(serializer.data)        
        
        
        