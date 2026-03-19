# <img width="326" height="94" alt="image" src="https://github.com/user-attachments/assets/d1cfbf62-273e-4d77-b0cf-48bf724ea1a4" /> (A Django Recipe Application) v1.4.2

## Table of Contents
- [Description](#description)
- [Key User Features](#-key-user-features)
  - [Future Features](#-future-features)
- [Using the Application](#-using-the-application)
  - [Homepage](#homepage)
  - [Login](#login)
  - [Sign Up](#sign-up)
  - [Recipe List](#recipe-list)
  - [Recipe Detail](#recipe-detail)
  - [Add Recipe](#add-recipe)
  - [Edit/Delete Recipes](#editdelete-recipes)
  - [Profile](#profile)
  - [Search](#search)
- [Setting Up Project Locally](#-setting-up-project-locally)
- [Technologies Used](#-technologies-used)
- [Change Log](#-change-log)


## Description:
A Python/Django application that users will be able to log into and interact with a recipe database.
   
<br>[Back to Table of Contents](#table-of-contents)

## ✅ Key User Features:
- Create an account
- Delete your account
- View list of all reicipes
- View details about a recipe
- **⭐Favorite a recipe/cook (new in v1.4.0)**
- Add a new recipe
- Edit/Delete your recipes
- Search for recipes by ingredient
- Profile Views
<br><br>
### 🔮 Future Features
- Sort recipe list filter
   
<br>[Back to Table of Contents](#table-of-contents)

## 🍴 Using the Application:

### Homepage
<img width="805" height="598" alt="image" src="https://github.com/user-attachments/assets/3c721edc-cf5c-492f-9c75-2f71b468f476" /><br>
The homepage displays links to login/signup for a user account, or browse the recipes.  Viewing the list of recipes is not a protected view but viewing details of the recipe is protected.
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

### Login
<img width="673" height="435" alt="image" src="https://github.com/user-attachments/assets/fd472f63-9d9c-4d02-b491-322043b9b7d3" /><br>
Registered users can enter credentials on the login page to gain access to protected views and add recipes to the database.
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

### Sign Up
<img width="673" height="424" alt="image" src="https://github.com/user-attachments/assets/1be3c7cb-d897-44f6-b8f6-023b65ad9d10" /><br>
Users can register for an account on the signup page with a username, password and confirming password.
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

### Recipe List
<img width="781" height="599" alt="image" src="https://github.com/user-attachments/assets/f410b34e-238b-48ef-a4b5-db1706cefb00" /><br>
The recipe list shows all stored recipes (in order of oldest to newest) displaying an image of the recipe.  Users can click on a recipe name or image to access the recipe details page for their selection.  A favorite toggle button ❤️ will be located in the bottom right corner of each image to add/remove the recipe as a favorite.

<p>Users will also be given more options in the menubar after they log in and can "Search" for recipes by an ingredient or "Add Recipe" to submit a new dish.</p>
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

⚠️*Note: Sorting recipe list not implemented in this release.*
<br><br>

### Recipe Detail
<img width="781" height="1070" alt="image" src="https://github.com/user-attachments/assets/3037e9a8-3947-485c-8c31-e88ab07a02cb" /><br>
The recipe detail view shows all the stored information about the recipe including who created it, last update, cooking time, difficulty level, ingredient list and instructions to prepare the dish.  If you are the owner of the recipe, you will be presented with the "Edit Recipe" and "Delete Recipe" buttons to update or remove your recipe.

<p>Recipes will show how many fans they have next to the favorite toggle button ❤️ near the recipe name heading.  Users can add the recipe as a favorite from the detail page or back on the listing page.  The cook named in the "Created By" field will also have a favorite toggle button ❤️ where users can add the cook to their favorites and see how many fans the cook has listed next to the heart button.</p>
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

### Add Recipe
<img width="679" height="884" alt="image" src="https://github.com/user-attachments/assets/17ca334c-8e13-4eef-8b4e-1db0fc46b6cc" /><br>
Authenticated users can add their own new recipes to the database by clicking "Add Recipe" in the menubar and completing the form above.  Instructions on formatting specifics given for best results in adding ingredients list and instructions.
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

### Edit/Delete Recipes
<img width="781" height="174" alt="image" src="https://github.com/user-attachments/assets/b90ea8d8-0b41-48f6-bef3-873b3778c7a7" /><br>
When viewing recipe details that the authenticated user created, the options for "Edit Recipe" and "Delete Recipe" will be presented.  Only the owner of the recipe will be able to access these buttons and modify/delete their own recipes. Choosing to delete a recipe will prompt user for confirmation prior to deleting as this cannot be undone. When choosing to edit the recipe, the user will be presented with the following screen where they can make changes:<br><br>
<img width="681" height="959" alt="image" src="https://github.com/user-attachments/assets/40ff735e-97f4-45dd-a6a5-035e33a7f03b" />
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

### Profile
<img width="781" height="599" alt="image" src="https://github.com/user-attachments/assets/d3d072b2-feb1-4e61-b4b4-e9aeb0c02256" /><br>
Users can view their profile after logging in by clicking the "Profile" option in the menubar or view another user's profile by clicking their name in a recipe detail page in the "Created By" field.  When viewing a profile, a list of that user's recipes, favorite recipes and favorite cooks will be shown in a section with tab headings for each category.  

<p>A favorite toggle button ❤️ will appear with a count of fans for the profile of the user you are viewing.  If viewing your own profile, this button will be disabled but still will show the number of fans.</p>

<p>If a user is viewing their own profile, they will have the option to delete their account.  This action must be confirmed on another page as this action cannot be undone.  Any user that deletes their account will lose ownership of all their recipes.  Their recipes will be retained in the database, but will now fall under "Deleted User" as the creator.  ⚠️*Note: These recipes can only be edited/removed via the Django Admin Console.* </p>
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

### Search
<img width="715" height="1619" alt="image" src="https://github.com/user-attachments/assets/a3b07af2-04f3-4f2a-8a87-4557af0122da" /><br>
Clicking "Search" on the bar brings the user to the search view where an ingredient (full or partial name) can be entered and the recipes containing that ingredient will be displayed.  The names of the recipes are links to the detailed recipe view for each. The page also displays some graphs with data showing how many recipes contain the ingredient, the overall distribution of difficulty level over all recipes and how many recipes users have contributed to the database.
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

## 🛠 Setting Up Project Locally:
1. You will need the following to begin setting up this application:
   - [Python](https://www.python.org/downloads/) 3.13 or later installed.
   - [Microsoft Azure](https://portal.azure.com/) 
   - Postgres database and access. *If you would like to use another relational database, you will need to update the `settings.py` for the database type.*
<br><br>

2. Clone repository onto your local machine: https://github.com/CincinnatiKid428/recipe-app.git
<br><br>

3. Create a virtual environment using Python:
   ```bash
    # Create a virtual environment
    python -m venv myenv
    
    # Activate it (Windows)
    myenv\Scripts\activate
    
    # Activate it (macOS/Linux)
    source myenv/bin/activate
    
    # Deactivate when done
    deactivate
   ```
   Or `pip install virtualenvwrapper` and use `mkvirtualenv myenv` to create the virtual environment.  If it does not automatically activate it, use `workon myenv` to activate it.
   Use `deactivate` to deactivate the virtual environment when finished.<br><br>
4. Activate your virtual environment and install dependencies with `pip install -r requirements.txt` from the project root folder.<br><br>
5. Create a `.env` file in the project root containing the following values:
   ```
     #Django 
     DJANGO_SECRET_KEY = 'YOUR-DJANGO-KEY'
     DEBUG=True #Enables debug mode for development

     #Azure Blob Storage
     AZURE_ACCOUNT_NAME = "YOUR-ACCOUNT"
     AZURE_ACCOUNT_KEY = "YOUR-AZURE-KEY"
     AZURE_CONTAINER = "media"

     #Database: Production (Neon.tech Postgres DB)
     #For SQLite dev database, comment out DATABASE_URL
     DATABASE_URL='postgresql://neondb_owner:YOUR-DATABASE-CONNECTION-STRING'
   ```
   ### In Development...
   - You will not need to use blob storage or Postgres database resources, you can use the Django SQLite database by commenting the `DATABASE_URL` variable above and change to development values in `settings.py` for `MEDIA_URL`,`MEDIA_ROOT`, and `DEFAULT_FILE_STORAGE`
   ### In Production...
   - You will need to configure blob storage and Postgres database resources.
   - *If you plan to use another blob storage and/or database host, you will need to update your `.env` as well as `settings.py` to configure for the application. Please note at the time of this release, Microsoft SQL Server was not supported by Python 3.13.*
   - The custom backend `recipes/storage_backends.py` contains class `MediaStorage` which is configured to use Microsoft Azure blob storage and will need to be updated to the blob storage of your choice.
  
6. If configured properly, you will need to run database migrations to setup tables (either in SQLite3 or Postgres).  From the root project folder, run commands:
  - `py manage.py makemigrations` (creates migrations file if not present)
  - `py manage.py migrate` (migrates database schema to the database)

7. If setup is successful and application configured properly, start the server from the project root folder with `py manage.py runserver` and you should be able to access the project via `https://localhost:8000` or `127.0.0.1:8000` in a web browser.
   
<br>[Back to Table of Contents](#table-of-contents)
<br><br>

## 🤖 Technologies Used:
- [Python](https://www.python.org/downloads/) v3.13.7
- [Django](https://www.djangoproject.com/) v5.2.7 
- [Bootstrap](https://getbootstrap.com/) v5.3.3
- [Bootstrap Icons](https://getbootstrap.com/) v1.11.3
- [Microsoft Azure](https://portal.azure.com/) Applicatin Hosting, Blob Storage
- [Neon](https://neon.tech/) Postgres Database Hosting

<br><br>
## 🚧 Change Log:
- v1.4.2 (3/18/2026): Added CSS to support mobile devices allowing better UI layout with new favorite toggle buttons.
- v1.4.1 (3/17/2026): Corrected staticfiles issue with "No Image" placeholder picture.
- v1.4.0 (3/17/2026):
     1. Added favorite recipes and cooks in a new UserProfile model for each user where users can add/remove entries using toggle buttons found in the application.
     2. Added favorite toggle buttons ❤️ to recipe listing page, recipe detail page and profile page to allow users to add recipes and/or cooks to their UserProfile as favorites.
     3. Added favorite recipes and favorite cooks in the profile page in a tabbed section that will display the favorites in a list and provide the link to go visit the recipe's detail page or the cook's profile page.  You may view other users' favorite recipes/cooks on their profile pages.
- v1.3.0 (1/10/2026): 
     1. Added hamburger menu with Bootstrap for mobile support and updated all template html files to use new navbar.
     2. Added "All Recipes" option to menu (also accessed by clicking Simmer logo when logged in)
- v1.2.0 (1/9/2026):
     1. Added Profile view feature where users can see a listing of recipes created by a selected user (or their own).
     2. Added ability for user to delete their own account via the Profile view screen.
     3. Detail view for a recipe will now show Created By user as a link to that user's profile unless it is "Deleted User".
     4. Menubar updated to add Profile option to authenticated users.
     5. Added Table of Contents to README.md for project.
- v1.1.1 (12/13/2025): Changed database field `ingredients` from CharField to TextField to allow for increased capacity.
- v1.1.0 (12/10/2025):
     1. Added edit/delete recipe functionality for owners to manage their recipes.
     2. "Back" button on recipe detail page to return to recipe list.
     3. Users will be directed to a recipe detail page if they tried to access it before logging in once they authenticate.
- v1.0.0 (11/30/2025): Initial release.
   
<br>[Back to Table of Contents](#table-of-contents)
