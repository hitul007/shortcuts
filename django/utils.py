from django.core.paginator import Paginator
from django.conf import settings as dj_settings

from rest_framework.response import Response


def create_response(data, code, message=None, extra={}):
    extra["media_url"] = dj_settings.MEDIA_URL
    return Response(
        {"data": data, "message": message, "code": code, "extra": extra}, code
    )


def pagination_on_queryset(queryset, page, per_page_items):
    if not per_page_items:
        per_page_items = 10

    p = Paginator(queryset, per_page_items)

    try:
        page_instance = p.page(page)
    except Exception:  # noqa
        return {"page_count": p.num_pages}

    return {"page_count": p.num_pages, "data": page_instance.object_list}

