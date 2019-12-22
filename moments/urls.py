"""wechat URL Configuration

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
from django.urls import path, re_path
from django.views.static import serve

import settings
from moments import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name="homepage.html")),
    path('status', views.show_status),
    path('user', views.show_user),
    path('post', views.show_post),
    path('exit', LogoutView.as_view(next_page="/")),
    path('register', views.register),
    path("user/update", views.update_user),
    path("like", views.like),
    path("comment", views.comment),
    path("comment/delete", views.delete_comment),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('report',views.report),
    path('stats',views.stats),
    path('friends',views.friends),

]
