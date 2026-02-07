"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blog import views as blog_views

urlpatterns = [
    path("", blog_views.home, name="home"),
    path("blog/", blog_views.blog_list, name="blog"),
    path("blog/<slug:slug>/", blog_views.blog_detail, name="blog_detail"),
    path("about/", blog_views.about, name="about"),
    path("contact/", blog_views.contact, name="contact"),
    path("terms/", blog_views.terms, name="terms"),
    path("privacy/", blog_views.privacy, name="privacy"),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
