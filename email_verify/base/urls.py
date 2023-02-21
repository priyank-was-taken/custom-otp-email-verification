from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.UserRegisterView.as_view(), name="user"),
    path('otp/', views.OtpVerificationView.as_view(), name="otp"),

]
