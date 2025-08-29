__all__ = [
    "app_name",
    "urlpatterns",
]

from django.urls import (
    URLPattern,
    path,
)

from django_mako_e2e.modules.samples.views import (
    CLSXIntegrationView,
    ClassBasedPartialRenderingView,
    ComponentSystemView,
    FunctionalPartialRenderingView,
    IndexView,
    ReadmeView,
)


app_name = "samples"

urlpatterns: list[URLPattern] = []

urlpatterns.extend(
    [
        path(
            "",
            IndexView.as_view(),
            name="index",
        ),
    ],
)

urlpatterns.extend(
    [
        path(
            "samples/clsx-integration/",
            CLSXIntegrationView.as_view(),
            name="clsx-integration",
        ),
    ],
)

urlpatterns.extend(
    [
        path(
            "samples/component-system/",
            ComponentSystemView.as_view(),
            name="component-system",
        ),
    ],
)

urlpatterns.extend(
    [
        path(
            "samples/partial-rendering/class-based/",
            ClassBasedPartialRenderingView.as_view(),
            name="class-based-partial-rendering",
        ),
        path(
            "samples/partial-rendering/functional/",
            FunctionalPartialRenderingView.as_view(),
            name="functional-partial-rendering",
        ),
    ],
)

urlpatterns.extend(
    [
        path(
            "samples/readme/",
            ReadmeView.as_view(),
            name="readme",
        ),
    ],
)
