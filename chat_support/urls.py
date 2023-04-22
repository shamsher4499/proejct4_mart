"""liquor_mart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_support_login, name="chat_support_login"),
    path('register/', views.chat_support_register, name="chat_support_register"),
    path('logout/', views.chat_support_logout, name="chat_support_logout"),
    path('chat/options/', views.chat_options, name="chat_options"),

    path('chat/with-ai/', views.chat_with_ai, name="chat_with_ai"),
    path('chat/with-ai/coming-soon/', views.coming_soon, name="coming_soon"),

    path('chat/with-human/create/room/', views.create_human_chat_room, name="create_human_chat_room"),
    path('chat/with-human/<str:room_slug>/', views.chat_with_human, name="chat_with_human"),

    path('chat/testing/', views.testing, name="testing"),


]
