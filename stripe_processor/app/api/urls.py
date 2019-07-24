# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from app.api import views

urlpatterns = [
    path('process-card', views.ProcessCardAPIView.as_view(), name='process_card')
]
