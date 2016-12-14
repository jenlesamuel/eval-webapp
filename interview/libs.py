from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse


def is_logged_in(request):
    '''
    Checks if a user has a valid session or not
    :param request: Django's request object
    :return bool Returns True if a user session exists, False otherwise
    '''

    try:
        token = request.session["interview"]["token"]

        if token:
            return True

        return False

    except KeyError:
        return False
