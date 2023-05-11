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
// postImgs.forEach((postImg) => {
//   postImg.addEventListener("mouseenter", () => {
//     const postBottom = postImg.nextElementSibling
//     postBottom.classList.remove('card-bottom-hidden')
//     });

//   postImg.addEventListener("mouseleave", () => {
//     const postBottom = postImg.nextElementSibling
//     postBottom.classList.add('card-bottom-hidden')
//     });

// })