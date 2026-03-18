/**
 * Filename: src/recipes/static/recipes/js/profile/favorites.js
 * 
 * Utility functions for CSS manipulation within profile.html template
 */

let recipes_btn;
let fav_recipes_btn;
let fav_cooks_btn;

let recipes_content;
let fav_recipes_content;
let fav_cooks_content;

//Once DOM is loaded...
document.addEventListener("DOMContentLoaded", () => {

  console.log('### Starting favorites.js|DOMContentLoaded...')

  //Get tab "button" HTML elements
  recipes_btn = document.getElementById("user_recipes_btn");
  fav_recipes_btn = document.getElementById("fav_recipes_btn");
  fav_cooks_btn = document.getElementById("fav_cooks_btn");

  //Get content HTML elements
  recipes_content = document.getElementById("user_recipes_div");
  fav_recipes_content = document.getElementById("fav_recipes_div");
  fav_cooks_content = document.getElementById("fav_cooks_div");

  //Add event listeners to all heart icons for toggle (Original function from ChatGPT)
  document.querySelectorAll(".favorite-btn").forEach(btn => {

    btn.addEventListener("click", function () {

      const type = this.dataset.type;
      const id = this.dataset.id;

      console.log(`### Adding event listner for type/id [${type}/${id}]`);

      fetch("/favorite-toggle/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `type=${type}&id=${id}`
      })
        .then(response => response.json())
        .then(data => {

          if (data.favorited) {
            this.classList.remove("bi-heart");
            this.classList.add("bi-heart-fill", "text-danger");
          } else {
            this.classList.remove("bi-heart-fill", "text-danger");
            this.classList.add("bi-heart");
          }

          const counter = document.getElementById(`count-${type}-${id}`);
          if (counter) counter.textContent = data.count;

        });

    });

  });

});

/**
 * Shows user's recipes on profile page.
 */
function showMyRecipes() {
  //Deactivate fav recipes
  deactivate(fav_recipes_btn);
  hideContent(fav_recipes_content);
  //Deactivate fav cooks
  deactivate(fav_cooks_btn);
  hideContent(fav_cooks_content);
  //Activate my recipes
  activate(recipes_btn);
  showContent(recipes_content);
}

/**
 * Shows favorite recipes on profile page.
 */
function showFavRecipes() {
  //Deactivate fav cooks
  deactivate(fav_cooks_btn);
  hideContent(fav_cooks_content);
  //Deactivate my recipes
  deactivate(recipes_btn);
  hideContent(recipes_content);
  //Activate fav recipes
  activate(fav_recipes_btn);
  showContent(fav_recipes_content);
}

/**
 * Shows favorite cooks on profile page.
 */
function showFavCooks() {
  //Deactivate fav recipes
  deactivate(fav_recipes_btn);
  hideContent(fav_recipes_content);
  //Deactivate my recipes
  deactivate(recipes_btn);
  hideContent(recipes_content);
  //Activate fav cooks
  activate(fav_cooks_btn);
  showContent(fav_cooks_content);
}


function activate(elem) {
  elem.classList.remove("profile-list-button-inactive");
  elem.classList.add("profile-list-button-active");
}

function deactivate(elem) {
  elem.classList.remove("profile-list-button-active");
  elem.classList.add("profile-list-button-inactive");
}

//Content show/hide functions:
function showContent(elem) { elem.classList.remove("element-hidden"); }
function hideContent(elem) { elem.classList.add("element-hidden"); }

//Helper function from ChatGPT
function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken"))
    .split("=")[1];
}


