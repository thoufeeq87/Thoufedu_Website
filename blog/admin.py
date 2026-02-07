from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from .models import AboutPage, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_at", "updated_at")
    search_fields = ("title", "body", "google_doc_url")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("content_preview", "created_at", "updated_at")
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "title",
                    "slug",
                    "status",
                    "google_doc_url",
                    "header_image",
                    "content_preview",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    formfield_overrides = {}

    def content_preview(self, obj):
        if not obj.content_html:
            return "No Google Docs content fetched yet."
        return format_html("{}", obj.content_html)

    content_preview.short_description = "Google Docs Content Preview"

    def save_model(self, request, obj, form, change):
        if obj.google_doc_url:
            try:
                obj.update_from_google_doc()
            except Exception as exc:
                raise ValidationError(str(exc)) from exc
        super().save_model(request, obj, form, change)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fields = ("title", "subtitle", "google_doc_url", "image")
    formfield_overrides = {}

    def save_model(self, request, obj, form, change):
        if obj.google_doc_url:
            try:
                obj.update_from_google_doc()
            except Exception as exc:
                raise ValidationError(str(exc)) from exc
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

# Register your models here.
