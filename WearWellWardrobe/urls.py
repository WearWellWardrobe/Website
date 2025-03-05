from django.urls import path, include
from WearWellWardrobe.views import PageGet
from WearWellWardrobe import views

# this is the local page one
app_name = "WearWellWardrobe"
urlpatterns = [
    path('items/', PageGet.as_view(), name='item-list'),
    #path('home/', views.home, name="home"),
    path('', views.home, name="home"),
    path("editPage/<slug:pageSlug>/", views.editPage, name="editPage"),
    path("deletePage/<slug:pageSlug>/", views.deletePage, name="deletePage"),
    path('addPage/', views.addPage, name='addPage'),
    path('editCategory/<slug:catSlug>/', views.editCategory, name='editCategory'),
    path('doneCategory', views.doneCategory, name='doneCategory'),
    path('register/', views.register, name='register'), 
    path('login/', views.user_login, name='login'),    
]