from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Ingredient

 
@login_required
def index(request):
    return render(request, 'cookbook/index.html')

@login_required
def new(request):
    message = ''
    m_position = 0
    ings = Ingredient.objects.filter(owner=request.user)
    ings = ings.order_by("category")
    if request.method == 'POST':
        name = request.POST['name']
        if name == '':
            message = "Recipe name field cannot be empty"
            m_position = 1

        image = request.POST['image']
        print(image.name)
        ing = request.POST.getlist('ing')

        type = request.POST['type']
        if type == 'Select dish type':
            message = "You must fill in the type of dish"
            m_position = 2

        serv = request.POST['servings']
        if serv == '':
            message = "Number of servings field cannot be empty"
            m_position = 3
        else:
            serv = int(serv)
            if (serv >= 1) and (serv % 10 == 0): 
                message = "Number of servings must be whole number and greater than 0"
                m_position = 3

        inst = request.POST['instruction']
        if inst == '':
            message = "Instruction field cannot be empty"
            m_position = 4
        
        if not message == '':
            return render(request, 'cookbook/new.html', {
                "message": message,
                "position": m_position,
                "name": name,
                "serv": serv, 
                "inst": inst, 
                "image": image   
            })


    
    return render(request, 'cookbook/new.html', {
        "ingredients": ings,
    })

@login_required
def ingredients(request):
    message = ''
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        owner = request.user
        if (name == '') or (category == ''):
            message = "Category and ingredient name fields cannot be empty"
        elif Ingredient.objects.filter(name=name): 
            message = "You already have ingredient with this name"
        else:
            i = Ingredient(name=name, category=category, owner=owner)
            i.save()

    ings = Ingredient.objects.filter(owner=request.user)
    ings = ings.order_by("category")
  
    return render(request, 'cookbook/ingredients.html', {
        "message": message,
        "ingredients": ings
    })

def delete_ing(request, name):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)  
    ing = Ingredient.objects.get(name=name)
    ing.delete()
    return JsonResponse({"message": f"Successfully delete ingredient {name}"})


@login_required
def about(request):
    return render(request, 'cookbook/about.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cookbook/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, 'cookbook/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cookbook/login.html", {
                "message": "Passwords must match.",
                'register': True
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cookbook/login.html", {
                "message": "Username already taken.",
                'register': True
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cookbook/login.html")
    




