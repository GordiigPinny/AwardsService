def get_token_from_request(request):
    try:
        return request.META.get['HTTP_AUTHORIZATION'][7:]
    except (IndexError, KeyError):
        return None
