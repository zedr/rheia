import functools


def cache_on_view(method):
    """A decorator that caches the value of properties or methods on views.
    """

    @functools.wraps(method)
    def inner(view, *args, **kwargs):
        storage = "__cached_" + method.__name__
        try:
            result = getattr(view, storage)
        except AttributeError:
            result = method(view, *args, **kwargs)
            setattr(view, storage, result)
        return result

    return inner
