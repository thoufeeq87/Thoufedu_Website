from django.conf import settings


def site_author(request):
    return {"site_author": getattr(settings, "SITE_AUTHOR", "")}
