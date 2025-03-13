"""projectSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from WearWellWardrobe import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'), # Should now redirect to login page
    path('WearWellWardrobe/',include("WearWellWardrobe.urls")), # Routes all links to the wearwellwardrobe url.py file
    path('api/', include(('WearWellWardrobe.urls', 'WearWellWardrobe'), namespace="WearWellWardrobe_api")),  # Route all API URLs to wear well wardrobe
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
