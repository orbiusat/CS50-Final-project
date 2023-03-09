from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Ingredient, Recipe

# Types of dish, user can choose for recipes. It goes straight to templates, where it fill select box
types = {'Salad', 'Soup', 'Snack', 'Main course', 'Bakery', 'Dessert', 'Sauce', 'Beverage', 'Bread'}


# Render index page
@login_required
def index(request):
    recipes = Recipe.objects.filter(owner=request.user)
    return render(request, 'cookbook/index.html', {
        "recipes": recipes
    })

# Render recipe page
@login_required
def recipe(request, id):
    recipe = Recipe.objects.get(pk=id)
    ingredients = recipe.ingredients.all()
    ingredients = ingredients.order_by("category")
    return render (request, 'cookbook/recipe.html', {
        "recipe": recipe,
        "ingredients": ingredients
    })

# API for deleting recipes
@login_required
def delete_recipe(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)  
    recipe = Recipe.objects.get(pk=id)
    recipe.delete()
    return HttpResponseRedirect(reverse("index"))

# Render page for adding new recipe
@login_required
def new(request):

    # Getting list of ingredients and setting default type of dish for template
    ings = Ingredient.objects.filter(owner=request.user)
    ings = ings.order_by("category")
    cur_type = 'Select dish type'

    # Adding new recipe into database
    if request.method == 'POST':
        # Var for message if something goes wrong, and it positon on a page. 
        message = ''
        m_position = 0

        # Checking that user fill all necessary fields
        name = request.POST['name']
        if name == '':
            message = "Recipe name field cannot be empty"
            m_position = 1

        cur_type = request.POST['type']
        if cur_type == 'Select dish type':
            message = "You must fill in the type of dish"
            m_position = 2

        serv = request.POST['servings']
        if serv == '':
            message = "Number of servings field cannot be empty"
            m_position = 3
        else:
            serv = int(serv)
            if (serv >= 1) and not(serv % 1 == 0): 
                message = "Number of servings must be whole number and greater than 0"
                m_position = 3

        inst = request.POST['instruction']
        if inst == '':
            message = "Instruction field cannot be empty"
            m_position = 4
        
        # Getting list of ingredients and image if user upload it
        new_ing = request.POST.getlist('ing')
        image = request.FILES.get('image', False)
        
        # If user does't fill some info, reload page with prefilled fields and error message
        if not message == '':
            return render(request, 'cookbook/new.html', {
                "message": message,
                "position": m_position,
                "name": name,
                "serv": serv, 
                "inst": inst,  
                "ingredients": ings,
                "types": types,
                "cur_type": cur_type,
                "current_ing": new_ing

            })

        # Adding new recipe into database
        r = Recipe(title=name, type=cur_type, serv=serv, inst = inst, owner=request.user)
        r.save()

        # Adding list of ingredietns and image into newly created recipe
        for ing in new_ing:
            i = Ingredient.objects.get(owner=request.user, name=ing)
            r.ingredients.add(i)
        if image: 
            r.image = image  
        r.save()
        return HttpResponseRedirect(reverse("index"))

    # Render page if method  = GET
    return render(request, 'cookbook/new.html', {
        "ingredients": ings,
        "types": types,
        "cur_type": cur_type
    })

# Render page for adding new recipe
@login_required
def edit (request, id):
    # Getting list of ingredients for template
    recipe = Recipe.objects.get(pk=id)
    ingredients = Ingredient.objects.filter(owner=request.user)
    current_ing = recipe.ingredients.all()

    # Handling save changes button
    if request.method == 'POST':
        # Var for message if something goes wrong, and it positon on a page. 
        message = ''
        m_position = 0

        name = request.POST['name']
        if name == '':
            message = "Recipe name field cannot be empty"
            m_position = 1

        serv = request.POST['servings']
        if serv == '':
            message = "Number of servings field cannot be empty"
            m_position = 3
        else:
            serv = int(serv)
            if (serv >= 1) and not(serv % 1 == 0): 
                message = "Number of servings must be whole number and greater than 0"
                m_position = 3

        inst = request.POST['instruction']
        if inst == '':
            message = "Instruction field cannot be empty"
            m_position = 4

        new_ing = request.POST.getlist('ing')
        image = request.FILES.get('image', False)
        type = request.POST['type']

        # If user does't fill some info, reload page with error message
        if not message == '':
            return render(request, 'cookbook/edit.html', {
                "message": message,
                "position": m_position,
                "recipe": recipe,
                "types": types,
                "ingredients": ingredients,
                "current_ing": current_ing,
              
            })

        # Change recipe data with new one
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

    # Render page if method  = GET
    return render (request, 'cookbook/edit.html', {
        "recipe": recipe,
        "ingredients": ingredients,
        "types": types,
        "current_ing": current_ing
    })

# Render ingredients page 
@login_required
def ingredients(request):
    message = ''

    # Adding new ingredient 
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

    # Getting ingredienst for template 
    ings = Ingredient.objects.filter(owner=request.user)
    ings = ings.order_by("category")
  
    return render(request, 'cookbook/ingredients.html', {
        "message": message,
        "ingredients": ings
    })

# API for deleting ingredients
def delete_ing(request, name):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)  
    ing = Ingredient.objects.get(name=name, owner=request.user)
    ing.delete()
    return JsonResponse({"message": f"Successfully delete ingredient {name}"})

# Render about page
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
    




