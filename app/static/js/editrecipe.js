const list = document.querySelector('.recipes');

let addstep = document.getElementById('addstep');
addstep.addEventListener('click', function (event) {
  let steps = document.querySelector('.recipe-header');
  let stepcount = steps.querySelectorAll('.slide').length - 1;
  console.log(stepcount);
  let prototype = document.getElementById('stepprototype');
  let clone = prototype.cloneNode(true);
  clone.innerHTML = `<h4><b>Step <input id="steps-${stepcount}-stepnumber" name="steps-${stepcount}-stepnumber" type="text" value="${stepcount + 1}"></b></h4>
                      <div class="recipe-detail" style="display: unset" id="steps-${stepcount}-steptext">
                        <p><input id="steps-${stepcount}-steptext" name="steps-0-steptext" required="" type="text" value=""></p>
                      </div>`
  steps.appendChild(clone);
})
// Function to copy the initial 'Add Ingredient' node when user presses Add Ingredient.
let addingredient = document.getElementById('addingredient');
addingredient.addEventListener('click', function (event) {
  let ingredients = document.querySelector('.ingredients');
  let ingredientcount = ingredients.querySelectorAll('.ingredient').length;
  let prototype = document.getElementById('ingredientprototype');
  let clone = prototype.cloneNode(true);
  clone.childNodes[1].id = `ingredients-${ingredientcount}-ingredient`;
  clone.childNodes[3].id = `ingredients-${ingredientcount}-unit`;
  clone.childNodes[5].id = `ingredients-${ingredientcount}-amount`;
  clone.childNodes[1].value = "";
  clone.childNodes[3].value = "";
  clone.childNodes[5].value = "";
  clone.childNodes[1].name = `ingredients-${ingredientcount}-ingredient`;
  clone.childNodes[3].name = `ingredients-${ingredientcount}-unit`;
  clone.childNodes[5].name = `ingredients-${ingredientcount}-amount`;
  ingredients.appendChild(clone);
})

// carousel
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

list.addEventListener('click', function(e) { // Function to delete a step
  let deletestep = e.target.closest('.deletestep');
  if (!deletestep) return;
  deletestep.parentElement.remove();
});

list.addEventListener('click', function(e) { // Function to delete a step
  let deleteing = e.target.closest('.deleteingredient');
  if (!deleteing) return;
  deleteing.parentElement.remove();
});
