const list = document.querySelector('.recipes');

let addstep = document.getElementById('addstep');
addstep.addEventListener('click', function (event) {
  let steps = addstep.parentElement;
  let stepcount = steps.querySelectorAll('.step').length;
  let prototype = document.getElementById('stepprototype');
  let clone = prototype.cloneNode(true);
  clone.childNodes[3].id = `steps-${stepcount}-steptext`;
  clone.childNodes[7].id = `steps-${stepcount}-stepnumber`;
  clone.childNodes[3].name = `steps-${stepcount}-steptext`;
  clone.childNodes[7].name = `steps-${stepcount}-stepnumber`;
  console.log(clone.childNodes)
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