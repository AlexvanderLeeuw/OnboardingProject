"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve as serve_static
from finance_manager.views import error_400, error_403, error_404, error_405, error_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finance_manager.urls')),
]

# DEBUG is False even in local development for this project (that's what makes
# the custom handler400/403/404/405/500 views below fire instead of Django's
# own debug pages), so runserver's automatic static handler never kicks in.
# Serve the collected static/ files (run `manage.py collectstatic` after
# changing anything under a static/ folder) explicitly instead.
urlpatterns += [
    re_path(r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), serve_static, {'document_root': settings.STATIC_ROOT}),
]

handler400 = error_400
handler403 = error_403
handler404 = error_404
handler405 = error_405
handler500 = error_500
