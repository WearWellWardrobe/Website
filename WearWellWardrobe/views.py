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

# from other pages
from WearWellWardrobe.models import Category, Page
from WearWellWardrobe.serializers import PageSerializer, ItemSerializer
from WearWellWardrobe.forms import PageForm, EditPageForm, EditCategoryForm, UserForm, UserProfileForm



def index(request):
    return render(request, "login.html")


# log in required for the rest of these -> once its set up

# the main page -> basically wants everything

def home(request):
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




        