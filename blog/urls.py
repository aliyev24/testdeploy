from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("categories/", views.categories, name="categories"),
    path("post/<slug:slug>/", views.post_detail, name="post-detail"),
]