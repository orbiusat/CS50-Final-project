from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Ingredient, Recipe

 
types = {'Salad', 'Soup', 'Snack', 'Main course', 'Bakery', 'Dessert', 'Sauce', 'Beverage'}

@login_required
def index(request):

    recipes = Recipe.objects.filter(owner=request.user)
    return render(request, 'cookbook/index.html', {
        "recipes": recipes
    })

@login_required
def recipe(request, id):
    recipe = Recipe.objects.get(pk=id)
    ingredients = recipe.ingredients.all()
    return render (request, 'cookbook/recipe.html', {
        "recipe": recipe,
        "ingredients": ingredients
    })

@login_required
def delete_recipe(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)  

    recipe = Recipe.objects.get(pk=id)
    recipe.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def edit (request, id):
    recipe = Recipe.objects.get(pk=id)
    ingredients = Ingredient.objects.filter(owner=request.user)
    current_ing = recipe.ingredients.all()

    if request.method == 'POST':
        message = ''
        m_position = 0
        name = request.POST['name']
        if name == '':
            message = "Recipe name field cannot be empty"
            m_position = 1

        new_ing = request.POST.getlist('ing')
        image = request.FILES.get('image', False)
        type = request.POST['type']

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
            return render(request, 'cookbook/edit.html', {
                "message": message,
                "position": m_position,
                "recipe": recipe,
                "types": types,
                "ingredients": ingredients,
                "current_ing": current_ing,
              
            })

        recipe.title = name
        recipe.type = type
        recipe.serv = serv
        recipe.inst = inst 

        recipe.ingredients.clear()
        for ing in new_ing:
            i = Ingredient.objects.get(owner=request.user, name=ing)
            recipe.ingredients.add(i)
        if image: 
            recipe.image = image  
        recipe.save()

        return HttpResponseRedirect(f"/recipe/{id}")


    return render (request, 'cookbook/edit.html', {
        "recipe": recipe,
        "ingredients": ingredients,
        "types": types,
        "current_ing": current_ing
    })

@login_required
def new(request):
    ings = Ingredient.objects.filter(owner=request.user)
    ings = ings.order_by("category")

    if request.method == 'POST':
        message = ''
        m_position = 0
        name = request.POST['name']
        if name == '':
            message = "Recipe name field cannot be empty"
            m_position = 1

        new_ing = request.POST.getlist('ing')
        image = request.FILES.get('image', False)

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
                "ingredients": ings
            })

        r = Recipe(title=name, type=type, serv=serv, inst = inst, owner=request.user)
        r.save()
        for ing in new_ing:
            i = Ingredient.objects.get(owner=request.user, name=ing)
            r.ingredients.add(i)
        if image: 
            r.image = image  
        r.save()
        return HttpResponseRedirect(reverse("index"))


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
        elif Ingredient.objects.filter(owner=request.user, name=name): 
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
    ing = Ingredient.objects.get(name=name, owner=request.user)
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
    




