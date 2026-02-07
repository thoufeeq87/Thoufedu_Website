from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from .models import AboutPage, Post


@cache_page(60 * 5)
def home(request):
    return render(request, "blog/landing.html")


@cache_page(60 * 2)
def blog_list(request):
    posts = list(
        Post.objects.filter(status=Post.STATUS_PUBLISHED).order_by("-created_at")
    )
    featured_post = posts[0] if posts else None
    grid_posts = posts[1:] if len(posts) > 1 else []
    return render(
        request,
        "blog/home.html",
        {
            "featured_post": featured_post,
            "grid_posts": grid_posts,
        },
    )


@cache_page(60 * 10)
def blog_detail(request, slug: str):
    post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.STATUS_PUBLISHED,
    )
    return render(request, "blog/detail.html", {"post": post})


@cache_page(60 * 10)
def about(request):
    about_page, _ = AboutPage.objects.get_or_create(pk=1)
    return render(request, "blog/about.html", {"about_page": about_page})


@cache_page(60 * 10)
def contact(request):
    return render(request, "blog/contact.html")


@cache_page(60 * 60)
def terms(request):
    return render(request, "blog/terms.html")


@cache_page(60 * 60)
def privacy(request):
    return render(request, "blog/privacy.html")
