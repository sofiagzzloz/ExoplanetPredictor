let slideIndex = 0;

function moveSlide(step) {
    const slides = document.getElementsByClassName("exoplanet-item");
    slideIndex += step;
    
    if (slideIndex >= slides.length) {
        slideIndex = 0;
    } else if (slideIndex < 0) {
        slideIndex = slides.length - 1;
    }

    const container = document.querySelector(".carousel-container");
    container.style.transform = `translateX(-${slideIndex * 100}%)`;
}