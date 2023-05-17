// 강의 캐러셀 
const courseSwiper = new Swiper(".course-curation", {
  slidesPerView: 2,
  spaceBetween: 3,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  breakpoints: {
    576: {
      slidesPerView: 2,
      spaceBetween: 3,
    },
    768: {
      slidesPerView: 3,
      spaceBetween: 5,
    },
    1024: {
      slidesPerView: 4,
      spaceBetween: 7,
    },
    1200: {
      slidesPerView: 5,
      spaceBetween: 10,
    },
  },
});

//  배너 
const bannerSwiper = new Swiper(".banner", {
  scrollbar: {
    el: ".swiper-scrollbar",
    hide: true,
  },
});

//  해시 
const hashSwiper = new Swiper('.hash-curation', {
  slidesPerView: 5,
  spaceBetween: 1,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  breakpoints: {
    576: {
      slidesPerView: 5,
      spaceBetween: 1,
    },
    768: {
      slidesPerView: 6,
      spaceBetween: 2,
    },
    1024: {
      slidesPerView: 8,
      spaceBetween: 3,
    },
    1200: {
      slidesPerView: 10,
      spaceBetween: 4,
    },
  },
});