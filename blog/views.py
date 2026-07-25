from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404
from . import models

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    fields = ["category", "title", "slug", "content", "excerpt", "cover_image", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def home(request):
    posts = models.Post.objects.filter(status=models.Post.Status.PUBLISHED).select_related("category")
    return render(request, "home.html", {
        "featured_post": posts.first(),
        "posts": posts[:6],
        "recent_posts": posts[:5],
        "categories": models.Category.objects.all(),
    })

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def categories(request):
    categories = models.Category.objects.all()
    active_category = None
    cat_slug = request.GET.get("cat")

    if cat_slug:
        active_category = get_object_or_404(models.Category, slug=cat_slug)
        posts = models.Post.objects.filter(
            status=models.Post.Status.PUBLISHED,
            category=active_category
        ).select_related("category")
    else:
        posts = models.Post.objects.filter(
            status=models.Post.Status.PUBLISHED
        ).select_related("category")

    return render(request, "categories.html", {
        "categories": categories,
        "active_category": active_category,
        "posts": posts,
        "total_posts": models.Post.objects.filter(status=Post.Status.PUBLISHED).count(),
    })



def post_detail(request, slug):
    post = get_object_or_404(models.Post, slug=slug, status=models.Post.Status.PUBLISHED)
    return render(request, "post_detail.html", {"post": post})

