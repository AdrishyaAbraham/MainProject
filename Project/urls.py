"""
URL configuration for Project project.

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
from django.urls import path,include
from school.views import *
from teacher.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', profile, name='profile'),
    path('update/', update_profile, name='update-profile'),
    # path('login/',include('django.contrib.auth.urls')),
    path('s/', include('school.urls')),
    path('teacher/', include('teacher.urls')),

    path('i/', index, name='indexdashboard'),
    path('t/',teacherdashboard, name='teacherdashboard'),
   
    path('st/',studentdashboard, name='studentdashboard'),
    path('d/',downloadresource, name='downloadresource'),
    path('',hoddashboard,name="hoddashboard"),
    # path('', login_page, name=''),
    # path('register/', register_page, name='register_page'),
    path('index1/', index1, name='index1'),
    path('index2', index2, name='index2'),
    path('logout/',logout,name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('social-auth/', include('social_django.urls', namespace='social')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   

