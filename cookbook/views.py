from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'cookbook/index.html')

def ingredients(request):
    return render(request, 'cookbook/ingredients.html')

def about(request):
    return render(request, 'cookbook/about.html')



