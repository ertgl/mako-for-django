__all__ = ["ClassBasedPartialRenderingViewTestCase"]

from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse


class ClassBasedPartialRenderingViewTestCase(TestCase):
    def test_class_based_view_renders_partial_mako_template(self) -> None:
        client = Client()
        response = client.get(
            reverse(
                "samples:class-based-partial-rendering",
                query={},
            ),
        )
        self.assertContains(
            response,
            "Class-based view.",
            count=1,
            status_code=200,
        )
