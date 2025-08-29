__all__ = ["IS_DJANGO_STUBS_EXT_PATCH_APPLIED"]

import django_stubs_ext


django_stubs_ext.monkeypatch()

IS_DJANGO_STUBS_EXT_PATCH_APPLIED = True
