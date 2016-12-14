import requests
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from requests.exceptions import RequestException

from interview.config import REMOTE_BASE_URL, LOGIN_PATH, TIME_OUT, HTTP_201_CREATED, REQUEST_PROCESSING_ERROR, HTTP_400_BAD_REQUEST,\
    INVALID_LOGIN_CREDENTIALS_ERROR, EVALUATIONS_PATH, HTTP_200_OK, HTTP_404_NOT_FOUND
from .forms import LoginForm


# Create your views here.


def index(request):
    pass


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
                    return HttpResponseRedirect(reverse("interview:list"))

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


def list(request):

    token = "Token "+str(request.session["interview"]["token"])
    headers = {"Accept": "application/json", "Authorization": token}
    url = "{}{}".format(REMOTE_BASE_URL, EVALUATIONS_PATH)
    error = ""

    try:
        response = requests.get(url, headers=headers, timeout=TIME_OUT)
        status_code = response.status_code

        if status_code == HTTP_200_OK:
            response_data = response.json()

            return render(request, "interview/list.html", {"records": response_data, "no_records":"No records found"})
            # display result
        else:
            error = REQUEST_PROCESSING_ERROR
            print(response.text)

    except RequestException as e:
        print("{}: {}".format(REQUEST_PROCESSING_ERROR, str(e)))
        error = REQUEST_PROCESSING_ERROR

    return render(request, "interview/processing_error.html", {"error": error})


def retrieve(request, id):
    token = "Token " + str(request.session["interview"]["token"])
    headers = {"Accept": "application/json"}
    data = {"id": id}
    url ="{}{}{}".format(REMOTE_BASE_URL, EVALUATIONS_PATH, id)

    try:
        response = requests.get(url, headers=headers, params=data, timeout=TIME_OUT)
        status_code = response.status_code

        if status_code == HTTP_200_OK:
            response_data = response.json()
            print(response_data)

            return render(request, "interview/evaluation.html", {})

        elif status_code == HTTP_404_NOT_FOUND:

            print(response.text)
            # find out how to dipaly 404 not found
            #return render(request, )




    except:
        pass



