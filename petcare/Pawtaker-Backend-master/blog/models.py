from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    description = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="pet_media/", max_length=254, null=True, blank=True
    )
    is_draft = models.BooleanField(default=True)
    published_date = models.DateTimeField()
    publisher_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    # excerpt is a short summary of the full description
    def get_excerpt(self):
        return self.description[:100]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.published_date = timezone.now()
        super(Blog, self).save(*args, **kwargs)
