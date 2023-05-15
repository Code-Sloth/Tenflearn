cardHover() 

export function cardHover() {
  const cards = document.querySelectorAll('.course-slide');
  cards.forEach((card) => {
    const slide = card.querySelector('.course-slide-hover');

    card.addEventListener('mouseenter', () => {
      slide.classList.remove('course-slide-hover-hidden');
    });

    card.addEventListener('mouseleave', () => {
      slide.classList.add('course-slide-hover-hidden');
    });
  });
}
