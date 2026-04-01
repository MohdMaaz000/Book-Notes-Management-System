from math import ceil


def build_pagination_meta(page: int, page_size: int, total_items: int) -> dict:
    total_pages = max(1, ceil(total_items / page_size)) if total_items else 1
    return {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }
