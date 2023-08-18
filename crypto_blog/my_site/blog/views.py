from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from datetime import date, datetime
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from .models import Post, Comment, Tag, SubscribedUsers
from .forms import CommentForm
from django.contrib import messages
import sweetify
# Create your views here.

#strona startowa
class Start(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "latest_post"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:5]
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now().date()
        context['tags'] = Tag.objects.all()


        for post in context['latest_post']:
            post.days_since_publication = (now - post.date).days
            post.tag_list = list(post.tags.values_list('caption', flat=True))  # Tworzy listę z nazwami tagów

        context['popular_posts'] = Post.objects.all().order_by('-views')[:3]

        return context

#strona z postem
class PostDetail(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.views += 1
        post.save()
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "tags": Tag.objects.all(),
            "counts":post.comments.count(),
            'popular_posts': Post.objects.all().order_by('-views')[:3]
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Comment aplied!")
            return redirect(request.META.get('HTTP_REFERER', reverse('start')))
        else:
            messages.success(request, "Please fill all the blank!")
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm,
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)

#strona ze wszystkimi postami
class All_posts(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    ordering = ["-date"]
    context_object_name = "all_posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()  # Pobierz wszystkie tagi
        context['popular_posts'] = Post.objects.all().order_by('-views')[:3]

        return context

#strona catogory wraz z pojedynczymi tagami
class CategoryView(View):
    def get(self, request, my_variable):
        posts = Post.objects.filter(tags__caption__contains=my_variable)
        tags = Tag.objects.all()
        context = {'category_post': posts, 'tags': tags, 'popular_posts':Post.objects.all().order_by('-views')[:3]}
        return render(request, "blog/category.html", context)

#strona contact wraz z tagami
class Contact(View):
    def get(self, request):
        tags = Tag.objects.all()
        context = {'tags': tags}
        return render(request, "blog/contact.html", context)

#strona about wraz z tagami
class About(View):
    def get(self, request):
        tags = Tag.objects.all()
        context = {'tags': tags,'popular_posts':Post.objects.all().order_by('-views')[:3]}
        return render(request, "blog/about.html", context)

#funkcja tworzenia subskrybcji
def subscribe(request):
    email = request.POST.get('email_to_subscribe', False)
    now = datetime.now().date()
    # email_to_subscribe = request.POST.get('email_to_subscribe')

    if SubscribedUsers.objects.filter(email=email).first():
        messages.success(request, "This email was subscribed before...")
    else:
        newsletter = SubscribedUsers(email=email, created_date=now)
        newsletter.save()
        messages.success(request, "Your email is subscribed!")

    # Przekierowanie na stronę kategorii
    return redirect(request.META.get('HTTP_REFERER', reverse('start')))

#wysyłanie wiadomosci poprzez strone contact
def send_message(request):
    name = request.POST.get('name', False)
    email_adress = request.POST.get('email', False)
    subject = request.POST.get('subject', False)
    message = request.POST.get('message', False)
    if name!='' and email_adress!='' and subject!='' and message!='':
        print(name,message,subject,email_adress)
        send_mail(
            subject,
            f"Imię: {name}\nEmail: {email_adress}\nWiadomość: {message}",
            settings.EMAIL_HOST_USER,
            ['konickiprzemyslaw@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "Message has been sent!")
    else:
        messages.success(request, "You have to fill the whole information!")
    return redirect(request.META.get("HTTP_REFERRER",reverse('contact')))
