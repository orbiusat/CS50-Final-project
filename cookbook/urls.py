from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("about", views.about, name="about"),
    path("new", views.new, name="new"),
    path("delete/ing/<str:name>", views.delete_ing, name="delete_ing"),
    path("recipe/<int:id>", views.recipe, name="recipe"),
    path("ingredients", views.ingredients, name="ingredients"),
]