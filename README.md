# Mako for Django

[Mako](https://www.makotemplates.org/) powered template backend for
[Django](https://www.djangoproject.com/).

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Installation](#installation)
- [Usage](#usage)
- [Tutorial](#tutorial)
- [References](#references)
- [Name](#name)
- [License](#license)

## Overview

This backend integrates Mako directly into Django's template engine API. It
supports Django's configuration, template discovery within app directories, and
context processors, while extending them with Mako's syntax, performance, and
detailed error handling.

<details>
  <summary>
    Preview: Contextual line information
  </summary>

  <picture>
    <img
      alt="TemplateSyntaxError preview"
      src="previews/template-syntax-error.png"
      width="100%"
      height="100%"
    />
  </picture>
</details>

<details>
  <summary>
    Preview: Runtime errors
  </summary>

  <picture>
    <img
      alt="Runtime error preview"
      src="previews/name-error.png"
      width="100%"
      height="100%"
    />
  </picture>
</details>

<details>
  <summary>
    Preview: Template postmortem
  </summary>

  <picture>
    <img
      alt="TemplateDoesNotExist preview"
      src="previews/template-does-not-exist.png"
      width="100%"
      height="100%"
    />
  </picture>
</details>

## Motivation

Mako's multi-zoned inheritance feature can be used with the `<%def>` tag to
encapsulate structure and behavior, enabling modular and maintainable
templates. This approach provides a component-like system similar to
[React](https://react.dev/)
([JSX](https://legacy.reactjs.org/docs/introducing-jsx.html)) or other modern
frameworks that support props and named/default slots. For technical details,
see the [Defs and Blocks](https://docs.makotemplates.org/en/latest/defs.html)
section in the Mako documentation.

### Demonstration

<details>
  <summary>
    Component definition: <code>button.html.mako</code>
  </summary>

  ```html
  <%def
    name="base_button(
      class_name=None,
      icon=None,
      label=None,
      round=False,
      rounded=False,
    )"
  >
    <button
      class="${ clsx([
        'button',
        ('button--round', round),
        ('button--rounded', rounded),
        class_name,
      ]) }"
    >
      % if icon:
        <span class="button__icon">
          ${ icon() }
        </span>
      % endif
      % if label:
        <span class="button__label">
          ${ label() }
        </span>
      % endif
    </button>
  </%def>

  <%def name="basic_button(class_name=None, rounded=False)">
    <%self:base_button
      class_name="${ ['button--basic', class_name] }"
      icon="${ getattr(caller, 'icon', None) }"
      label="${ getattr(caller, 'label', None) }"
      rounded="${ rounded }"
    />
  </%def>

  <%def name="icon_button(class_name=None, round=False)">
    <%self:base_button
      class_name="${ ['button--icon', class_name] }"
      icon="${ getattr(caller, 'body', None) }"
      round="${ round }"
    />
  </%def>
  ```

  > The `clsx` function is a utility for managing class-names dynamically. It's
  > imported from the
  > <a href="https://github.com/ertgl/clsx-py" target="_blank">clsx-py</a>
  > project.
</details>

<details>
  <summary>
    Component usage: <code>page.html.mako</code>
  </summary>

  ```html
  <%namespace name="button" file="button.html.mako" />

  <%button:icon_button class_name="sample-button">
    ➖
  </%button:icon_button>

  <%button:icon_button class_name="sample-button" round="${ True }">
    ➕
  </%button:icon_button>

  <%button:basic_button class_name="sample-button">
    <%def name="icon()">✖️</%def>
    <%def name="label()">Cancel</%def>
  </%button:basic_button>

  <%button:basic_button class_name="sample-button" rounded="${ True }">
    <%def name="icon()">⚡</%def>
    <%def name="label()">Trigger</%def>
  </%button:basic_button>
  ```
</details>

<details>
  <summary>
    Output
  </summary>

  ```html
  <button class="button button--icon sample-button">
    <span class="button__icon">➖</span>
  </button>

  <button class="button button--round button--icon sample-button">
    <span class="button__icon">➕</span>
  </button>

  <button class="button button--basic sample-button">
    <span class="button__icon">✖️</span>
    <span class="button__label">Cancel</span>
  </button>

  <button class="button button--rounded button--basic sample-button">
    <span class="button__icon">⚡</span>
    <span class="button__label">Trigger</span>
  </button>
  ```
</details>

## Installation

Available on PyPI:

```sh
pip install mako-for-django
```

## Usage

Minimal configuration in `settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django_mako.MakoEngine",
        "DIRS": [
            BASE_DIR / "mako",
        ],
        "APP_DIRS": True,
        "OPTIONS": {},
    },
]
```

> [!IMPORTANT]
> By default, templates within apps should be placed under a `mako` directory.

<details>
  <summary>
    Example: Extending <code>OPTIONS</code>
  </summary>

  ```python
  MAKO_LOOKUP_OPTIONS = {
    "cache_enabled": True,
    # https://beaker.readthedocs.io/en/latest/
    "cache_impl": "beaker",
  }

  MAKO_TEMPLATE_OPTIONS = {
    "encoding_errors": "strict" if DEBUG else "htmlentityreplace",
  }

  TEMPLATES = [
      {
          "BACKEND": "django_mako.MakoEngine",
          "DIRS": [
              BASE_DIR / "mako",
          ],
          "APP_DIRS": True,
          "OPTIONS": {
              "lookup": {
                  **MAKO_LOOKUP_OPTIONS,
              },
              "template": {
                  **MAKO_TEMPLATE_OPTIONS,
              },
          },
      },
  ]
  ```
</details>

<details>
  <summary>
    Example: Using Mako alongside DjangoTemplates
  </summary>

  ```python
  SHARED_TEMPLATE_CONTEXT_PROCESSORS = [
      "django.template.context_processors.debug",
      "django.template.context_processors.request",
      "django.contrib.auth.context_processors.auth",
      "django.template.context_processors.tz",
      "django.template.context_processors.i18n",
      "django.contrib.messages.context_processors.messages",
      "django.template.context_processors.static",
      "django.template.context_processors.media",
  ]

  # Context processors to use with Mako backend only.
  MAKO_TEMPLATE_CONTEXT_PROCESSORS = [
      "django_mako.template.context_processors.url",
  ]

  TEMPLATES = [
      {
          "BACKEND": "django_mako.MakoEngine",
          "DIRS": [
              BASE_DIR / "mako",
          ],
          "APP_DIRS": True,
          "OPTIONS": {
              "context_processors": [
                  *SHARED_TEMPLATE_CONTEXT_PROCESSORS,
                  *MAKO_TEMPLATE_CONTEXT_PROCESSORS,
              ],
          },
      },
      {
          "BACKEND": "django.template.backends.django.DjangoTemplates",
          "DIRS": [
              BASE_DIR / "templates",
          ],
          "APP_DIRS": True,
          "OPTIONS": {
              "context_processors": [
                  *SHARED_TEMPLATE_CONTEXT_PROCESSORS,
              ],
          },
      },
  ]
  ```
</details>

## Tutorial

This tutorial guides you through creating a minimal Django project using Mako
templates. Follow the steps to set up the project, add an application, create
layout and page templates, and finally render a simple page in the browser.

By the end of this tutorial, the project structure should look like this:

```txt
demo/
├── demo/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── index/
│   ├── mako/
│   │   └── index/
│   │       └── views/
│   │           └── index.html.mako
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── mako/
│   └── layout.html.mako
└── manage.py
```

1. Create a new Django project:

```sh
django-admin startproject demo
cd demo
```

2. Create a new app inside the project:

```sh
python manage.py startapp index
```

3. Enable the app in `settings.py`:

```python
INSTALLED_APPS = [
    "index",
]
```

4. Configure `MakoEngine` in `settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django_mako.MakoEngine",
        "DIRS": [
            BASE_DIR / "mako",
        ],
        "APP_DIRS": True,
        "OPTIONS": {},
    },
]
```

5. Add layout template `mako/layout.html.mako`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title><%block name="title">Demo</%block></title>
  </head>
  <body>
    ${ next.body() }
  </body>
</html>
```

6. Create page template `index/mako/index/views/index.html.mako`:

```html
<%inherit file="/layout.html.mako" />

<%block name="title">${ title } | ${ parent.title() }</%block>

<h1>${ title }</h1>
```

7. Add view in `index/views.py`:

```python
from django.shortcuts import render


def index(request):
    return render(
        request,
        # The template path, relative to `index/mako` directory.
        "/index/views/index.html.mako",
        {
            "title": "Mako for Django",
        },
    )
```

8. Wire up `urls.py`:

```python
from django.urls import path
from index.views import index


urlpatterns = [
    path("", index),
]
```

9. Run the server:

```sh
python manage.py runserver
```

After running the server, you can visit
[http://127.0.0.1:8000/](http://127.0.0.1:8000/).

<details>
  <summary>
    Checkout the <code>e2e</code> directory for more examples.
  </summary>

  ```sh
  git clone https://github.com/ertgl/mako-for-django.git
  cd mako-for-django/e2e
  make
  python manage.py runserver
  ```
</details>

## References

- [Mako Templates for Python](https://www.makotemplates.org/)
- [Templates | Django documentation](https://docs.djangoproject.com/en/5.2/topics/templates/)
- [How to implement a custom template backend | Django documentation](https://docs.djangoproject.com/en/5.2/howto/custom-template-backend/)
- [django/template/backends - django/django on GitHub](https://github.com/django/django/tree/550822bceea227b07445d1852c4376b663c09ea4/django/template/backends)

## Name

Published on PyPI as `mako-for-django`. The import name `django_mako` is chosen
for brevity.

## License

This project is licensed under the
[MIT License](https://opensource.org/license/mit).
See the [LICENSE](LICENSE) file for details.
