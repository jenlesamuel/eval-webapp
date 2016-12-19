import requests
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from requests.exceptions import RequestException
from interview.config import REMOTE_BASE_URL, LOGIN_PATH, TIME_OUT, HTTP_201_CREATED, REQUEST_PROCESSING_ERROR, HTTP_400_BAD_REQUEST,\
    INVALID_LOGIN_CREDENTIALS_ERROR, EVALUATIONS_PATH, HTTP_200_OK, HTTP_404_NOT_FOUND, RESOURCE_NOT_FOUND
from .forms import LoginForm
from .libs import is_logged_in


# Create your views here.

def login(request):

    error = ""

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            headers = {"Content-Type": "application/json", "Accept" : "application/json"}
            payload = {"username": email, "password": password}


            try:
                url = "{}{}".format(REMOTE_BASE_URL, LOGIN_PATH)
                response = requests.post(url, json=payload, headers=headers, timeout=TIME_OUT)
                status_code = response.status_code

                if status_code == HTTP_400_BAD_REQUEST:
                    # TODO : LOG response.text
                    error = INVALID_LOGIN_CREDENTIALS_ERROR
                    print(response.text)

                elif status_code == HTTP_201_CREATED:
                    # The end point returns 201 on success.
                    response_data = response.json()
                    token = response_data['token']
                    request.session['interview'] = {"token": token}
                    print(token)
                    return HttpResponseRedirect(reverse("interview:index"))

                else:
                    # Handle other HTTP response codes
                    error = REQUEST_PROCESSING_ERROR
                    print(response.text)


            except RequestException as e:
                # Handle exceptions while executing request
                # TODO: Log error
                print("{}: {}".format(REQUEST_PROCESSING_ERROR , str(e)))
                error = REQUEST_PROCESSING_ERROR


    else:
        login_form = LoginForm()

    return render(request, 'interview/login.html', {'form': login_form, "error": error})


def index(request):

    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("interview:login"))

    token = "Token "+str(request.session["interview"]["token"])
    headers = {"Accept": "application/json", "Authorization": token}
    url = "{}{}".format(REMOTE_BASE_URL, EVALUATIONS_PATH)
    error = ""

    try:
        response = requests.get(url, headers=headers, timeout=TIME_OUT)
        status_code = response.status_code

        if status_code == HTTP_200_OK:
            response_data = response.json()

            return render(request, "interview/list.html", {"records": response_data, "no_records": "No records found"})
            # display result
        else:
            error = REQUEST_PROCESSING_ERROR
            print(response.text)

    except RequestException as e:
        print("{}: {}".format(REQUEST_PROCESSING_ERROR, str(e)))
        error = REQUEST_PROCESSING_ERROR

    return render(request, "interview/processing_error.html", {"error": error})


def retrieve(request, id):

    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("interview:login"))

    token = "Token " + str(request.session["interview"]["token"])
    headers = {"Accept": "application/json", "Authorization": token}
    data = {"id": id}
    url ="{}{}{}".format(REMOTE_BASE_URL, EVALUATIONS_PATH, id)
    error = ""

    try:
        response = requests.get(url, headers=headers, params=data, timeout=TIME_OUT)
        status_code = response.status_code

        if status_code == HTTP_200_OK:
            response_data = response.json()
            print(response_data)

            return render(request, "interview/evaluation.html", {"record": response_data})

        elif status_code == HTTP_404_NOT_FOUND:

            print(response.text)
            error = RESOURCE_NOT_FOUND

        else:

            print(response.text)
            error = REQUEST_PROCESSING_ERROR

    except RequestException as e:

        print("{}: {}".format(REQUEST_PROCESSING_ERROR, str(e)))
        error = REQUEST_PROCESSING_ERROR

    return render(request, "interview/processing_error.html", {"error": error})

def logout(request):
    try:
        if request.session["interview"]:
            del request.session["interview"]
    except KeyError:
        pass

    return HttpResponseRedirect(reverse("interview:login"))







