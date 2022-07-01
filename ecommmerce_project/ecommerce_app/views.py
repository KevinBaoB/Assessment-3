from urllib import response
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# pip install request
import requests as HTTP_Client
# pip install requests_oauthlib
from requests_oauthlib import OAuth1
# pip install python-dotenv to read .env
from dotenv import load_dotenv
# Create your views here.
import pprint
import os
# Create your views here.

def index(request):
    response = render(request, 'ecommerce_app/home.html')
    return response

def inventory(request):
    response = render(request, 'ecommerce_app/inventory.html')
    return response

def cart(request):
    response = render(request, 'ecommerce_app/cart.html')
    return response

def get_icon(request, name):
    auth = OAuth1(os.environ["apikey"], os.environ["privatekey"])
    endpoint = f"http://api.thenounproject.com/icon/{name}"

    API_response = HTTP_Client.get(endpoint, auth=auth)
    responseJSON = API_response.json()
    # print(API_response.content)
    # print(responseJSON)
    # pp.pprint(responseJSON)
    icon = (responseJSON['icon']['preview_url'])
    if os.environ['env'] == 'prod':
        # send emails, only ibn prod
        pass