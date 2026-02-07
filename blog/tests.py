from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogListViewTests(TestCase):
    def test_blog_list_shows_only_published_posts(self):
        Post.objects.create(
            title="Draft post",
            body="Draft body",
            status=Post.STATUS_DRAFT,
        )
        published = Post.objects.create(
            title="Published post",
            body="Published body",
            status=Post.STATUS_PUBLISHED,
        )

        response = self.client.get(reverse("blog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, published.title)
        self.assertNotContains(response, "Draft post")

# Create your tests here.
