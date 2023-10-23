from django.urls import path
from api import views

urlpatterns = [
    path("auth/register", views.register),
    path("auth/login", views.login),
    path("allUsers", views.allUsers),
    path("getUser", views.getUser),
    path("updateUser", views.updateUser),
    path("deleteUser", views.deleteUser),
]
