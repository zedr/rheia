def wants_json(request):
    """Discover if a request wants JSON for the response.
    """
    accept_header = request.META.get("HTTP_ACCEPT", None)
    if accept_header and accept_header.startswith("application/json"):
        return True
    else:
        return False
