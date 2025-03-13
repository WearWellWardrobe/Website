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
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

# from other pages within the site
from WearWellWardrobe.models import Category, Page
from WearWellWardrobe.serializers import PageSerializer, ItemSerializer
from WearWellWardrobe.forms import PageForm, EditPageForm, EditCategoryForm, UserForm, UserProfileForm



def index(request):
# the main page that all basic entry requests are sent to
    return render(request, "login.html")


# log in should be required for the rest of these

def home(request):
# the main home page - lists everything

    categories = Category.objects.all()
    context_dict = {'category': categories}
    try:
        pages = Page.objects.all()
        cats = Category.objects.all()
        context_dict['pages'] = pages
        context_dict['category'] = cats
    
    except:
        pass

    return render(request, "loggedInHome.html", context=context_dict)


def viewPage(request, pageSlug):
# shows each page, but not in use?

    context = {}
    try:
        pageData = Page.objects.get(slug=pageSlug)
        context["page"] = pageData
    except Page.DoesNotExist:
        context["page"] = None
    return render(request, "", context=context)


def editPage(request, pageSlug):
# editPage view -> redirect back to home page once done    
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
# a holder page for once the category has been edited. maybe have it redirect back to edit category
    return render(request, "categroyDone.html")

def editCategory(request, catSlug):
# this page appears in an iframe tag that allows the user to edit the category. acts like a dropdown box, but is an actual page
# requires data about the category it is responsible for

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
        
        
        
        
# delete request
def deletePage(request, pageSlug):
# perhaps put some validation within this view to see if the page is actually alowed to be deleted, and not a user getting around the URLs
    pageData = Page.objects.get(slug=pageSlug)

    if request.method == "POST":
        pageData.delete()
        return redirect("WearWellWardrobe:home") 

    return render(request, "delete.html", {"page": pageData})
   
class PageGet(APIView):
# the main API to get all the page data
    def get(self, request):
        pages = Page.objects.all()
        serializer = ItemSerializer(pages, many=True)
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = '*'  
        return response
        

class PageListView(ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
        
class RecordDetail(APIView):
    def get(self, request, pk, format=None):
        # Fetch the record by primary key (pk)
        item = get_object_or_404(Item, pk=pk)
        
        # Serialize the item and return as JSON
        serializer = ItemSerializer(item)
        return Response(serializer.data)        
        
        
def register(request):
# sign up page
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'register.html',context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
# sign in page
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('WearWellWardrobe:home'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            messages.error(request, "Invalid login details. Please try again.")
            return redirect('WearWellWardrobe:login')  # Redirect back to the login page
    else:
        return render(request, 'login.html')




        