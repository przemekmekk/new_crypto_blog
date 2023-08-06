from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.Start.as_view(), name="start"),
    path("all-posts",views.All_posts.as_view(), name="all-posts"),
    path("category/<str:my_variable>/", views.CategoryView.as_view(), name="category"),
    path("contact", views.Contact.as_view(), name="contact"),
    path("about", views.About.as_view(), name="about"),
    path("posts/<slug:slug>", views.PostDetail.as_view(), name="post"),
    path("subscribe",views.subscribe,name="subscribe"),
    path("send_message", views.send_message, name="send_message"),

    # path("category/<str:my_variable>/subscribe", views.subscribe, name="subscribe")

    # path("subscribe_two", views.subscribe_two, name="subscribe_two")
    # path("blog-details", views.Blog_details.as_view(), name="blog-details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)