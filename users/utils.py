
def get_user_from_request(request):
    if request.user.is_anonymous:
        return None
    else:
        return request.user