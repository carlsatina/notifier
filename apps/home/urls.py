# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views, notification

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Single Notification
    path('single/<int:user_id>', notification.single, name='single-notification'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
