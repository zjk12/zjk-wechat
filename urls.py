# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import re_path
from django.views.static import serve

import settings

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^account/', include('blueapps.account.urls')),
    # 如果你习惯使用 Django 模板，请在 home_application 里开发你的应用，
    # 这里的 home_application 可以改成你想要的名字
    url(r'^', include('moments.urls')),
    # 如果你习惯使用 mako 模板，请在 mako_application 里开发你的应用，
    # 这里的 mako_application 可以改成你想要的名字
    url(r'^mako/', include('mako_application.urls')),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
