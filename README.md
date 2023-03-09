# YOUR PROJECT TITLE
#### Video Demo:  https://youtu.be/dV4TeO7_bbI
#### Description:
CookBook - is a Web App, that works like recipe book. User’s can add new recipes, change existing ones and delete those they no longer need. They also have access to personalize list of ingredients, they can add and delete. The difference from other apps that contain same functional is it orientation on private use. Where all recipe related apps works almost like social network, and sharing recipes is they primary feature, CookBook app allows to keep user’s recipes private and work more like old time kitchen recipe book.

I’m use Django framework for python and a little of JavaScript on that project, so most of the code contained in views.py. Here lies all functions that handle rendering of pages.

For database I use Django models. Models used in this project you can find inf models.py. As it still on a simpler side, I use only three models. One for app users, one for ingredients and one for recipes.

For my JS a create five different files. They mostly correspond with different pages of app.
ing.js contains code to async request to server that delete ingredient from database.
login.js contains DOM manipulation for login page. It switches register form with login form depending on click of a button.
nav.js contains code for navbar, that set couple attributes making navbar responsive.
new.js contains code for custom select and also some image manipulation.
recipe.js contains code to async request to server that delete recipe from database and a little function for making textarea that contains instruction change height depending on content.
