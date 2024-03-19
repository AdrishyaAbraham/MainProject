from django.urls import path
from flutterapp import views


urlpatterns = [
    path('login/',views.login, name='login'),

]
