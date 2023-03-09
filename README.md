# COOKBOOK
#### Video Demo:  https://youtu.be/dV4TeO7_bbI
#### Description:
CookBook - is a Web App, that works like a recipe book. User’s can add new recipes, change existing ones, and delete those they no longer need. They also have access to personalize list of ingredients, they can add and delete. The difference from other apps that contain same functional is it orientation on private use. Where all recipe related apps works almost like social network, and sharing recipes is their primary feature, CookBook app allows keeping user’s recipes private and work more like old time kitchen recipe book.

I’m use Django framework for python and a little of JavaScript on that project, so most of the code contained in views.py. Here lies all functions that handle rendering of pages.
For database, I use Django models. Models used in this project, you can find inf models.py. As it still on a simpler side, I use only three models. One for app users, one for ingredients and one for recipes.

Django also demands to declare every path in web app at separate file. It named urls.py	

When I run into problem with clearing images from OS, when corresponding db entry is removed. To resolve it, I use Django CleanupConfig. 

For my JS I create five different files. They mostly correspond with different pages of app.
ing.js contains code to async request to server that delete ingredient from database, and it also deletes it representation on a page right away. 
login.js contains DOM manipulation for login page. It switches register form with login form depending on click of a button.
nav.js contains code for navbar, that set couple attributes making navbar responsive.
new.js contains code for custom select and also some image manipulation. Have function that translate image into img tag in two cases: one with using browse option, and one using drag & drop. 
recipe.js contains code to async request to server that delete recipe from database and a little function for making textarea that contains instruction change height depending on content.

The thing I’m proud of is that I finally understand how I can save images in database and how I can use dynamically on a page via JavaScript. For now, though, it lacks an option to add image via URL. I plan to add this functional later. 

Also, I see a problem with that user can’t add an amount of each ingredient he adds. On plus sign it streamlines creation of new recipe, but on the other hand it’s not very practical. And it also would'n work with current select design. If I have to change only one thing about my project, it would be that. 

App also have responsive design. It achieved mostly through CSS media queries. Only exception is navbar witch use a little JS. Though I don’t test app on real phones, only with developer tools. 

For all images I use third party assets, and on “Credit” page I mention all the beautiful people that provide it for me. Some of the icons I change slightly to match over all app design.  

I hope you enjoy using CookBook! 
