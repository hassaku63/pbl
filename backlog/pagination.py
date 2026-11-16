# coding: utf-8
"""
Iterate over every item of a paginated list endpoint.

Backlog API list endpoints page their results in one of two ways:

- offset and count (issues, documents, watchings, pull requests, ...): iterate_by_offset()
- minId / maxId, count and order (activities, notifications, comments, stars, wiki history, ...): iterate_by_id()

Both call the list method repeatedly, one page per request, and yield the items one by one. They stop after
a page that has fewer items than requested. The rate limit handling of BacklogAPI (rate_limit_retries)
applies to every request.

    from backlog.pagination import iterate_by_offset
    for issue in iterate_by_offset(api.issue.list, **{"projectId[]": [1]}):
        ...

Most resources also have iter...() methods built on these, e.g. api.issue.iter().
"""

MAX_COUNT = 100


def iterate_by_offset(fetch, *args, count=MAX_COUNT, offset=0, **kwargs):
    """
    Yield the items of a list method that takes offset and count.

    :param fetch: the list method, e.g. api.issue.list
    :param args: positional arguments for the method
    :param count: (int) items per request (1-100), default 100
    :param offset: (int) offset of the first item, default 0
    :param kwargs: other arguments for the method (filters, sort, order, ...)
    """
    while True:
        page = fetch(*args, offset=offset, count=count, **kwargs)
        yield from page
        if len(page) < count:
            return
        offset += len(page)


def iterate_by_id(fetch, *args, count=MAX_COUNT, order="desc", **kwargs):
    """
    Yield the items of a list method that takes minId, maxId, count and order.

    With order="desc" (the API default) items are yielded from the newest; with order="asc" from the oldest.
    Pass minId and/or maxId to limit the range.

    :param fetch: the list method, e.g. api.activity.list
    :param args: positional arguments for the method
    :param count: (int) items per request (1-100), default 100
    :param order: (str) "desc" (default) or "asc"
    :param kwargs: other arguments for the method
    """
    if order not in ("asc", "desc"):
        raise ValueError('order must be "asc" or "desc"')
    bound = "minId" if order == "asc" else "maxId"
    seen = set()
    while True:
        page = fetch(*args, count=count, order=order, **kwargs)
        # The next request starts at the last ID of this page. Whether the API includes that boundary item
        # or not, skipping the IDs already yielded avoids both gaps and duplicates.
        for item in page:
            if item["id"] not in seen:
                seen.add(item["id"])
                yield item
        if len(page) < count:
            return
        last = page[-1]["id"]
        if kwargs.get(bound) == last:
            return  # no progress: a page of only the boundary item
        kwargs[bound] = last


def id_range(minId=None, maxId=None):
    """
    The minId / maxId keyword arguments that are set, for passing on to iterate_by_id().
    """
    return {k: v for k, v in (("minId", minId), ("maxId", maxId)) if v is not None}
