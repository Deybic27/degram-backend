"""
URL configuration for degram_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dg_user.urls import urlpatterns_dg_user
from dg_auth.urls import urlpatterns_dg_auth
from dg_media.urls import urlpatterns_dg_media
from dg_recommended.urls import urlpatterns_dg_recommended
from dg_post.urls import urlpatterns_dg_post
from dg_api.urls import urlpatterns_dg_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urlpatterns_dg_user)),
    path('api/', include(urlpatterns_dg_auth)),
    path('api/', include(urlpatterns_dg_media)),
    path('api/', include(urlpatterns_dg_recommended)),
    path('api/', include(urlpatterns_dg_post)),
    path('api/', include(urlpatterns_dg_api)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
