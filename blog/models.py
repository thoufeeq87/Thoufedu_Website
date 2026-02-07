import re
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.db import models
from django.utils.html import strip_tags
from django.utils.text import slugify


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._chunks.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self._chunks).split())


class Post(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHED, "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    header_image = models.ImageField(upload_to="blog_headers/", blank=True)
    body = models.TextField(blank=True)
    google_doc_url = models.URLField(blank=True)
    content_html = models.TextField(blank=True)
    content_text = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    @property
    def summary(self) -> str:
        return self.content_text or strip_tags(self.body or "")

    def update_from_google_doc(self) -> None:
        doc_id = self._extract_doc_id(self.google_doc_url)
        if not doc_id:
            raise ValueError("Invalid Google Docs URL.")

        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=html"
        request = Request(export_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")

        cleaned = self._sanitize_html(html)
        extractor = _TextExtractor()
        extractor.feed(cleaned)

        self.content_html = cleaned
        self.content_text = extractor.text()
        if not self.body:
            self.body = self.content_text

    @staticmethod
    def _extract_doc_id(url: str) -> str | None:
        if not url:
            return None
        parsed = urlparse(url)
        if "docs.google.com" not in parsed.netloc:
            return None
        match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", parsed.path)
        return match.group(1) if match else None

    @staticmethod
    def _sanitize_html(html: str) -> str:
        without_scripts = re.sub(
            r"<(script|style)[^>]*>.*?</\1>",
            "",
            html,
            flags=re.DOTALL | re.IGNORECASE,
        )
        without_events = re.sub(r"\son\w+\s*=\s*\"[^\"]*\"", "", without_scripts)
        without_js = re.sub(r"javascript:", "", without_events, flags=re.IGNORECASE)
        return without_js

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200] or "post"
            slug = base_slug
            counter = 2
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Me")
    subtitle = models.CharField(max_length=300, blank=True)
    body = models.TextField(blank=True)
    google_doc_url = models.URLField(blank=True)
    content_html = models.TextField(blank=True)
    content_text = models.TextField(blank=True)
    image = models.ImageField(upload_to="about/", blank=True)

    def __str__(self) -> str:
        return "About Page"

    @property
    def summary(self) -> str:
        return self.content_text or strip_tags(self.body or "")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = 1
        super().save(*args, **kwargs)

    def update_from_google_doc(self) -> None:
        doc_id = self._extract_doc_id(self.google_doc_url)
        if not doc_id:
            raise ValueError("Invalid Google Docs URL.")

        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=html"
        request = Request(export_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")

        cleaned = self._sanitize_html(html)
        extractor = _TextExtractor()
        extractor.feed(cleaned)

        self.content_html = cleaned
        self.content_text = extractor.text()
        if not self.body:
            self.body = self.content_text

    @staticmethod
    def _extract_doc_id(url: str) -> str | None:
        if not url:
            return None
        parsed = urlparse(url)
        if "docs.google.com" not in parsed.netloc:
            return None
        match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", parsed.path)
        return match.group(1) if match else None

    @staticmethod
    def _sanitize_html(html: str) -> str:
        without_scripts = re.sub(
            r"<(script|style)[^>]*>.*?</\1>",
            "",
            html,
            flags=re.DOTALL | re.IGNORECASE,
        )
        without_events = re.sub(r"\son\w+\s*=\s*\"[^\"]*\"", "", without_scripts)
        without_js = re.sub(r"javascript:", "", without_events, flags=re.IGNORECASE)
        return without_js

# Create your models here.
