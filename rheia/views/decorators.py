def redirect_to(url, force=True):
    def _outer(view_func):
        def _inner(request, *args, **kwargs):
            if "next" not in request.POST or force:
                request.REQUEST.dicts += ({"next": url},)
            return view_func(request, *args, **kwargs)

        return _inner

    return _outer
