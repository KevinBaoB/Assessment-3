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
    response = render(request, 'ecommerce_app/index.html')
    return response