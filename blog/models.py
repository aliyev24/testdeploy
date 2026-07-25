from django.conf import settings
from django.db import models
from django.urls import reverse



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True, max_length=500)
    cover_image = models.ImageField(upload_to="posts/covers/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED