const cards = document.querySelectorAll('.course-slide')


cards.forEach((card) => {
  card.addEventListener("mouseenter", () => {
    const slide = card.querySelector('.course-slide-hover')
    slide.classList.remove('course-slide-hover-hidden')
  });

  card.addEventListener("mouseleave", () => {
    const slide = card.querySelector('.course-slide-hover')
    slide.classList.add('course-slide-hover-hidden')
  });


})
