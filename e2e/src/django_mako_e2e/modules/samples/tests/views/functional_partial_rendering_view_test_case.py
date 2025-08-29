__all__ = ["FunctionalPartialRenderingViewTestCase"]

from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse


class FunctionalPartialRenderingViewTestCase(TestCase):
    def test_functional_view_renders_partial_mako_template(self) -> None:
        client = Client()
        response = client.get(
            reverse(
                "samples:functional-partial-rendering",
                query={},
            ),
        )
        self.assertContains(
            response,
            "Functional view.",
            count=1,
            status_code=200,
        )
