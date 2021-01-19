const menuBtn = document.querySelector('.menu-btn');
const menu = document.getElementById('menu');
let menuOpen = false;
menuBtn.addEventListener('click', () => {
  if(!menuOpen) {
    $("#menu").fadeIn(); // Fade in the menu when clicking button
    menuOpen = true;
    menuBtn.classList.add("open"); // Apply CSS trick to animate button
  }
  else {
    $("#menu").fadeOut(); // Fade out the menu
    menuOpen = false;
    menuBtn.classList.remove("open"); // Remove CSS trick - de-activate button. 
  }
});