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
  }
  recipe.classList.add('recipes-active'); // And activate selected.
});


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

const form = document.getElementById('stepsform');
const submit = document.getElementById('submitstep');
const next = document.getElementById('nextstep');
const steps = document.getElementById('steps');
const addsteps = document.getElementById('addsteps');
let stepText = document.getElementById('steptext');
let stepCount = document.getElementById('stepcount');
addsteps.addEventListener('click', () => {
  console.log('hello');
  $("#stepsform").fadeIn();
})
submit.addEventListener('click', () => {
  var step = document.createElement("div");
  step.classList.add('step');
  step.innerHTML = stepText.value;
  step.setAttribute("name", `Step ${steps.childElementCount}`);
  steps.appendChild(step);
  stepText.value = "";
  stepCount.setAttribute("name", steps.childElementCount)
  $(form).fadeOut();
});
next.addEventListener('click', () => {
  var step = document.createElement("div");
  step.classList.add('step');
  step.innerHTML = stepText.value;
  step.setAttribute("name", `Step ${steps.childElementCount}`);
  steps.appendChild(step);
  stepCount.setAttribute("name", steps.childElementCount)
  stepText.value = "";
});
