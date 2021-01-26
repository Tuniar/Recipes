// Function to activate / de-activate menu-cards (bring into focus / expand)

const list = document.querySelector('.recipes');
const recipes = document.querySelectorAll('.recipe');
list.addEventListener('click', function (event) { // Listen for clicks on the recipes grid

  let recipe = event.target.closest('.recipe');
  if (!recipe) return;
  let slide = event.target.closest('.active-slide');
  if (slide) return;
  if (!list.contains(recipe)) return;
  if (recipe.classList.contains('recipes-active')) { // If you're clicking on the active one, deactivate it and return. 
    recipe.classList.remove('recipes-active');
    return; 
  }
  for (i = 0; i < recipes.length; i++)
  {
    recipes[i].classList.remove('recipes-active'); // Otherwise deactivate all currently active...
    let ingredients = recipes[i].querySelector('.ingredients')
    $(ingredients).fadeOut();
  }
  recipe.classList.add('recipes-active'); // And activate selected.
  let ingredients = recipe.querySelector('.ingredients')
  $(ingredients).fadeIn();
});

// Function to carousel through slides. 

list.addEventListener('click', function(e) {// Listen for clicks on recipes grid
  if (!e.target.closest('.recipes-active')) return;
  let recipe = e.target.closest('.recipe');
  let slide = e.target.closest('.slide');
  if (!slide) return;
  let slides = slide.parentElement.querySelectorAll('.slide');
  let slideCount = slide.parentElement.childElementCount;
  let index = $(slide).index();
  if (index == slideCount -1)
  {
    slide.classList.remove('active-slide');
    slides[0].classList.add('active-slide');
  }
  else {
    slide.classList.remove('active-slide');
    slides[index + 1].classList.add('active-slide');
  }
});

//Expand search box when button clicked (and contract create box, if open)

const searchb = document.getElementById('searchb');
const search = document.getElementById('search');
let searchOpen = false;
searchb.addEventListener('click', () => {
  createOpen = false;
  $("#create").fadeOut();
  if(!searchOpen) {
    $("#search").fadeIn(); // Fade in the search form when clicking button
    searchOpen = true;
  }
  else {
    $("#search").fadeOut(); // Fade out the search form
    searchOpen = false;
  }
});

//Expand create box when button clicked (and contract search box, if open)

const createb = document.getElementById('createb');
const create = document.getElementById('create');
let createOpen = false;
createb.addEventListener('click', () => {
  searchOpen = false;
  $("#search").fadeOut();
  if(!createOpen) {
    $("#create").fadeIn(); // Fade in the create form when clicking button
    createOpen = true;
  }
  else {
    $("#create").fadeOut(); // Fade out the create form
    createOpen = false;
  }
});

// Add steps to recipe form, with correctly incremented name attribute to be read by the form.

let addstep = document.getElementById('addstep');
addstep.addEventListener('click', function (event) {
  let steps = addstep.parentElement;
  let stepcount = steps.querySelectorAll('.step').length;
  let prototype = document.getElementById('stepprototype');
  let clone = prototype.cloneNode(true);
  console.log(clone);
  clone.childNodes[3].id = `steps-${stepcount}-steptext`;
  clone.childNodes[7].id = `steps-${stepcount}-stepnumber`;
  clone.childNodes[3].name = `steps-${stepcount}-steptext`;
  clone.childNodes[7].name = `steps-${stepcount}-stepnumber`;
  steps.appendChild(clone);
})
// Function to copy the initial 'Add Ingredient' node when user presses Add Ingredient.
let addingredient = document.getElementById('addingredient');
addingredient.addEventListener('click', function (event) {
  let ingredients = addingredient.parentElement;
  let ingredientcount = ingredients.querySelectorAll('.ingredient').length;
  let prototype = document.getElementById('ingredientprototype');
  let clone = prototype.cloneNode(true);
  clone.childNodes[1].id = `ingredients-${ingredientcount}-ingredient`;
  clone.childNodes[3].id = `ingredients-${ingredientcount}-unit`;
  clone.childNodes[5].id = `ingredients-${ingredientcount}-amount`;
  clone.childNodes[1].name = `ingredients-${ingredientcount}-ingredient`;
  clone.childNodes[3].name = `ingredients-${ingredientcount}-unit`;
  clone.childNodes[5].name = `ingredients-${ingredientcount}-amount`;
  ingredients.appendChild(clone);
})

// Search to auto-fill grid when searching for recipes by name.
// Note this stopped working when the objects became "complex" (relational)
// TO DO: implement searching by ingredient in same way.
let input = document.querySelector('#rname');
input.addEventListener('keyup', function() {
    $.get('/recipes?q=' + input.value, function(recipes) {
      let html = '';
      for (let recipe in recipes)
      {
          console.log(recipes)
          let name = recipes[recipe].recipename;
          let desc = recipes[recipe].recipedesc;
          html += `<div class="recipe">
                    <img class="" src="static/images/bbb.jpg" alt="${name}">
                    <div class="recipe-header" id="bbb">
                      <div class="slide active-slide">
                        <h4><b>${name}</b></h4>
                        <div class="recipe-detail">
                          <p>${desc}</p>
                        </div>
                      </div>
                      <div class="slide">
                        <h4><b></b></h4>
                        <div class="recipe-detail">
                          
                        </div>
                      </div>
                          
                    </div>
                  </div>`
      };

      document.querySelector('.recipes').innerHTML = html;
    });
});