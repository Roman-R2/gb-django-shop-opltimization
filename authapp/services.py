def check_next_in_request(request):
    """
    Проверяет наличие слова 'next' в объекте запроса request методе POST
    :param request:
    :return:
    """
    return True if 'next' in request.POST else False
