from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.caption}"

    class Meta:
        verbose_name_plural = "Tags"

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_adress = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class Post(models.Model):
    title = models.CharField(max_length=45)
    type = models.CharField(max_length=150, default=None)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts")
    image_all_posts = models.ImageField(upload_to="posts", null=True, blank=True)
    image_slider = models.ImageField(upload_to="posts", null=True, blank=True)
    image_side_popular_post = models.ImageField(upload_to="posts", null=True, blank=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    content_1 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_2 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_3 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_4 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_5 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_6 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_7 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_8 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_9 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    content_10 = models.TextField(validators=[MinLengthValidator(0)],null=True,blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)
    views = models.PositiveIntegerField(default=0)
# funkcja z aktywnymi linkami:
    def get_absolute_url(self):
        return reverse("detail",args=[self.slug])

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    user_name = models.CharField(max_length=120, blank=False, null=False)
    user_email = models.EmailField(blank=False, null=False)
    text = models.TextField(max_length=400, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")


class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField("Data created", default=timezone.now)

    def __str__(self):
        return f"{self.email}"
