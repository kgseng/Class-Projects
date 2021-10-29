// Name: Kenny Seng
// Assignment: Project
// Slide js and timings made with and adapted from W3 schools & medium.com
//  W3 Schools: https://www.w3schools.com/howto/howto_js_slideshow.asp
//  Medium: https://medium.com/better-programming/make-a-slideshow-with-automatic-and-manual-controls-using-html-css-and-javascript-b7e9305168f9

var slideIndex = 1;
var myTimer;

// On page load, slide show starts at slide 1; timer sent for 3000 ms.
window.addEventListener("load",function() {
    showSlides(slideIndex);
    myTimer = setInterval(function(){plusSlides(1)}, 3000);
})

// next & prev
function plusSlides(n){
    clearInterval(myTimer);
    // Decrement slide
    if (n < 0){
        showSlides(slideIndex -= 1);
    }
    // Increment slide
    else {
        showSlides(slideIndex += 1);
    }

    // if slide is negative, interval must fixed by two slides worth of time
    if (n === -1){
        myTimer = setInterval(function(){plusSlides(n + 2)}, 3000);
    }
    else {
        myTimer = setInterval(function(){plusSlides(n + 1)}, 3000);
    }
}

// current slide, resets intervals as necessary
function currentSlide(n){
    clearInterval(myTimer);
    myTimer = setInterval(function(){plusSlides(n + 1)}, 3000);
    showSlides(slideIndex = n);
}

function showSlides(n){
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");

    // if slide counter goes beyond slide length, reset to first slide
    if (n > slides.length) {slideIndex = 1}
    // if slide counter goes before first slide, reset to last slide
    if (n < 1) {slideIndex = slides.length}

    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
    }
    // display slide
    slides[slideIndex-1].style.display = "block";
}
